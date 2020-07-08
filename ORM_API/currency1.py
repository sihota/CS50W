import requests

def main():
    url = "https://api.exchangeratesapi.io/latest?base=EUR&symbols=CAD,USD"
    #url2 = "http://data.fixer.io/api/latest?access_key="+APIKEY+"&symbols=USD&format=1"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Error API request unsuccessful!")
    data = response.json()
    rate = data["rates"]["CAD"]
    print(f"1 EUR is equal to {rate} CAD")

if __name__ == "__main__":
    main()
