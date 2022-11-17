import graphene
from graphene_django import DjangoObjectType
from app.models import Building
import requests
import re


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building
        fields = ("__all__")


class AddData(graphene.Mutation):
    status = graphene.Int()
    message = graphene.String()

    class Arguments:
        zipcode = graphene.String()
        address = graphene.String()

    def mutate(root, info, zipcode='', address=''):
        print("=======> FETCHING DATA FROM DATASET")
        url = "https://data.cityofnewyork.us/resource/8y4t-faws.json?"
        queryData = '$query=SELECT zip_code, block, lot, land_area, yrbuilt, bldg_class, owner, housenum_lo, housenum_hi, street_name WHERE '
        if zipcode:
            queryData += f"zip_code='{zipcode}' AND "
        if address:
            addressDetails = address.upper().replace(",", "").strip()
            addressDetails = addressDetails.rstrip("NY")
            addressDetails = addressDetails.rstrip("NEW YORK")
            addressDetails = addressDetails.split()
            if addressDetails[1] in ['W', 'E', 'S', 'N']:
                addressDetails[1] = f"{addressDetails[1]}%"
            addressData = ' '.join(addressDetails[1:])
            addressData = re.sub(r"(?<=\d)(ST|ND|RD|TH)\b",
                                 '', addressData).strip().upper()
            queryData += f"(housenum_lo='{addressDetails[0]}' AND street_name LIKE '{addressData}%')"
        print(url+queryData)
        headers = {
            "Accept": "application/json",
            "X-App-Token": "0du1uYQrSXbx5f2gzvBNFEMN1"
        }
        response = requests.get(url+queryData, headers=headers)
        print("=======> DATA FETCHED")
        data = response.json()
        newData = [dict(t) for t in {tuple(d.items()) for d in data}]
        print("=======> PARSING DATA", len(newData), len(data))
        print("=======> SAVING INTO DATABASE")
        for building in newData:
            try:
                buildingDetails = {
                    "address": address,
                    "zipcode": zipcode,
                    "block_number":  building.get('block'),
                    "lot": building.get('lot'),
                    "lot_sq_ft": building.get('land_area'),
                    "year_built": building.get('yrbuilt'),
                    "building_class": building.get('bldg_class'),
                    "owner": building.get('owner'),
                }
                buildingData = Building(**buildingDetails)
                buildingData.save()
                status = 200
                message = "All building data is saved"
            except Exception as e:
                status = 400
                message = "Something went wrong!"
                print("Error", e)
        print("=======> DATA SAVED IN DATABASE")
        return AddData(status=status, message=message)


class Mutation(graphene.ObjectType):
    add_data = AddData.Field()


class Query(graphene.ObjectType):
    all_buildings_data = graphene.List(BuildingType)
    buildings_by_address = graphene.Field(
        BuildingType, address=graphene.String(required=True))

    def resolve_all_buildings_data(root, info):
        print("=======> FETCHING ALL BUILDING DATA")
        return Building.objects.all()

    def resolve_buildings_by_address(root, info, address):
        try:
            print("=======> FETCHING BUILDING DATA BY ADDRESS")
            return Building.objects.get(address=address)
        except Building.DoesNotExist:
            return None


schema = graphene.Schema(query=Query, mutation=Mutation)
