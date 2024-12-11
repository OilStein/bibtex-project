import requests
from citation import Citation

refs = []

while True:

    c = input("give command[add, list, quit]: ")

    if c == "quit":
        break

    elif c == "add":
        doi = input("give doi: ")

        data = requests.post('https://dl.acm.org/action/exportCiteProcCitation', data={
        'dois': doi,
        'targetFile': 'custom-bibtex',
        'format': 'bibTex'
        }).json()["items"][0][doi]

        author = " and ".join([f"{person['family']}, {person['given']}" for person in data["author"]])

        obj = Citation(data["title"], author, data["original-date"]["date-parts"][0][0])

        refs.append(obj)

        print(data)

    elif c == "list":
        for ref in refs:
            print(ref.print_as_bibtex())

# doi = "10.5555/2387880.2387905"

# r = requests.post('https://dl.acm.org/action/exportCiteProcCitation', data={
#         'dois': doi,
#         'targetFile': 'custom-bibtex',
#         'format': 'bibTex'
#     })


# print(r.json()["items"])