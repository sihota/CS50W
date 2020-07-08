import requests

def main():
    response = requests.get("https://google.com/",verify=False)
    print(response.text)

if __name__ == "__main__":
    main()
