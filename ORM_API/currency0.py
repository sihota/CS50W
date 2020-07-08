import requests

def main():
    APIKEY = ""
    response = requests.get("http://data.fixer.io/api/latest?access_key="+APIKEY+"&symbols=USD&format=1")
    if response.status_code != 200:
        raise Exception("Error API request unsuccessful!")
    data = response.json()
    print(data)

if __name__ == "__main__":
    main()
