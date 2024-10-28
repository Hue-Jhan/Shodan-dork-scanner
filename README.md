# Shodan & Censys IOT scanner
Multitool that scans all kinds of devices on the internet such as servers, iot, web servers, databases and more using Censys and Shodan api. Also contains a list of useful queries to use.

# 💻 Code

<img align="right" src="media/iot2hue1.png" width="400" />
The code is just a multitool-styled menu with options:

- **Censys Search**: uses censys api to lookup specific devices on the internet, you can specify the number of results.
- **Censys host info**: uses censys api to get informations on a specific devices. more info on the #scanner section.
- **Shodan info**: uses shodan free api (which kinda sucks) to lookup iot devices on the web.
- **Queries examples**: shows a long list of examples of queries to lookup on shodan, censys or google dork.


# 📡 Scanner

<img align="right" src="media/iot2hue2.png" width="300" />

```Censys Search```: The first scanner uses censys api as i said before, it's not as complete as the shodan one but it does its job, the api key is free to obtain on their website. Sorry if the results in the example are your apache servers XD.

In order to get the api to work i sent the credentials as b64 encoded headers during the get request for the ip, i don't even know what i did but it works so dont complain, the requests is then shown, and every "service" of the ip is listed. The service can be an open port, a vulnerability or anything like that.

Be aware that some shodan queries might not work on Censys website and some might not work used via api, dont ask me why.

```Censys host info```: The second scanner works

# 📋 Queries
The query list is just a list of examples taken from websites and github pages. 

