import json

f1 = open("./contract/abi/ZINKmarket.json", "r")
f2 = open("./contract/abi/ZINKOrderContract.json", "r")

abi1 = json.load(f1)
abi2 = json.load(f2)

ZINKmarketApi = []
ZINKOrderContractApi = []

def getApi(abi) -> list:
    api = []
    for i in abi:
        if i["type"] == "function":
            api.append([i["name"]] + [i["inputs"]])
    return api

ZINKmarketApi = getApi(abi1)
ZINKOrderContractApi = getApi(abi2)
# print(ZINKmarketApi)
# print(ZINKOrderContractApi)
def printApiList(apiList):
    for name, inputArgs in apiList:
        argsStr = ""
        for item in inputArgs:
            argsStr += item["type"] + " " + item["name"] + ","
        argsStr = argsStr[:-1]
        print(f"{name}({argsStr})")

printApiList(ZINKmarketApi)
print("*" * 10)
printApiList(ZINKOrderContractApi)