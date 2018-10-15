import  requests
class proxy_generator:
    generate_url='http://30376382046574422.standard.hutoudaili.com/?num=100'

    def generate(self):
        data=requests.get(self.generate_url)
        return data.text.split('\r\n')
