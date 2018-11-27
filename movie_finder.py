import json, requests, os, sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        movie_title = ' '.join(sys.argv[1:])
    else:
        print('PLease input movie name')
        movie_title = input(str())

    APIKEY = 'f18b8f11'
    BASEURL = "http://omdbapi.com"

    def imdb_request(movie_title, apikey, baseurl):

        try:
            response = requests.get(baseurl, params={'apikey': apikey, 't': movie_title})
        except IOError as e:
            raise e("Some problems with requested url!")

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise ValueError("Bad request!")


    def movie_saver(movie):

        path = 'movie_info'
        posters_dir = 'movie_posters'
        posters_path = '\\'.join((path, posters_dir))
        title = movie['Title']

        os.makedirs(path, exist_ok=True)
        os.makedirs('movie_info\\movie_posters', exist_ok=True)

        movie_data = dict(year=movie['Year'], genre=movie['Genre'],
                          director=movie['Director'], plot=movie['Plot'])

        if movie['Poster'] != 'N/A':
            img = requests.get(movie['Poster']).content
            with open((posters_path + '\\' + title + '.jpg'), 'wb+') as handler:
                handler.write(img)

        with open('\\'.join((path, 'movie_title.txt')), 'a+') as handler:
            handler.seek(0)
            lines = handler.readlines()
            if f'{title}: \n' in lines:
                handler.close()
            else:
                handler.seek(2)
                handler.write('\n' + title + ': \n')
                handler.writelines(f' {i}: {movie_data[i]} \n' for i in movie_data)

        return 'Movie_info was successfully updated'

    movie = imdb_request(movie_title, APIKEY, BASEURL)
    if 'Error' in movie:
        print(movie['Error'])
    else:
        print(movie_saver(movie))

