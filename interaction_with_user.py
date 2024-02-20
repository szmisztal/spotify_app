import urllib


class UserInteraction:
    def user_album_and_artist_inputs(self):
        album_input = self.user_input_parser(input("Album: "))
        artist_input = self.user_input_parser(input("Artist: "))
        return (album_input, artist_input)

    def playlist_name_input(self):
        playlist_name = input("Set your playlist name: ")
        return playlist_name

    def user_input_parser(self, user_input):
        parsed_input = urllib.parse.quote(user_input)
        return parsed_input

