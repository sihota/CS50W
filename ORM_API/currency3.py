import requests

def main():
    #APIKEY = ""
    base = input("First Currency: ")
    other = input("Other Currency: ")
    url = "?base=EUR&symbols=CAD,USD"
    #url2 = "http://data.fixer.io/api/latest?access_key="+APIKEY+"&symbols=USD&format=1"
    response = requests.get("https://api.exchangeratesapi.io/latest",
                    params={"base":base,"symbols":other})

    if response.status_code != 200:
        raise Exception("Error API request unsuccessful!")
    data = response.json()
    rate = data["rates"][other]
    print(f"1 {base} is equal to {rate} {other}")

if __name__ == "__main__":
    main()
