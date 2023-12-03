<!-- Improved compatibility of back to top link: See: https://github.com/ri0t/mqttnotifier/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPLv3 License][license-shield]][license-url]
[![LiberaPay][liberapay-shield]][liberapay-url]
[![Patreon][patreon-shield]][patreon-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ri0t/mqttnotifier">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">MQTT Notifier</h3>

  <p align="center">
    An awesome MQTT notification daemon to display popup notifications from MQTT!
    <br />
    <a href="https://github.com/ri0t/mqttnotifier"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ri0t/mqttnotifier/issues">Report Bug</a>
    ·
    <a href="https://github.com/ri0t/mqttnotifier/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#configuration">Configuration</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![MQTT Notifier Screen Shot][screenshot]](https://github.com/ri0t/mqttnotifier)

I was looking for solutions to display popup notifications from Home Assistant (and others, hence MQTT) and only found a Windows based solution, so i quickly wrote this one.

Using paho-mqtt, it connects to a given MQTT broker, subscribes to a given topic and uses plyer to display sender-configurable notification popups from published messages. The payload it expects is a simple JSON object containing some freely configurable parameters along with the message body.

These configurable items are:

* Application Title
* Popup Title
* Message body
* Timeout
* Application Icon

Very handy!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python (3.5+ should work, developed with 3.11)
* [paho-mqtt](https://github.com/eclipse/paho.mqtt.python)
* [plyer](https://github.com/kivy/plyer)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

* Grab the software
* Install dependencies and mqttnotifier
* Configure mqttnotifier
* Test your broker connection
* Install as service
* Receive notifications!

### Prerequisites

This is what you need to use the software:

* a working Python 3.7+ installation 
* along with a rather recent pip3
* python-dbus is required by plyer

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ri0t/mqttnotifier.git
   ```
2. Generate virtual environment
   ```sh
   mkvirtualenv mqttnotifier
   ```
3. Install Python packages and mqttnotifier
   ```sh
   pip3 install .
   ```
4. Test if it works - until there's a test suite, just run it
   ```sh
   mn --help
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Configuration -->
## Configuration

`mn` accepts configuration data in three ways:

* command line arguments (run `mn --help` or `mn launch --help`)
* environment variables (at least for MN_USERNAME and MN_PASSWORD)
* configuration file

A [sample configuration file](https://github.com/ri0t/mqttnotifier/blob/master/example_config.toml) is provided.

Command line arguments supersede configuration entries and environment variables supersede command line arguments.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

To run it as daemon, use
   ```sh
   mn launch
   ```

To test if it works, run the `test` command:
   ```sh
   mn test
   ```

You can also increase verbosity (lower number = higher verbosity) to debug problems:
   ```sh
   mn -v 5 launch
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add test suite
- [ ] Verify platform independence (it should run on all platforms that support paho-mqtt and plyer)
  - [ ] Maybe write installation/usage instructions for other platforms
- [ ] Verify python versions (it uses typings, so at least 3.5 is necessary, there are backports for some functionality, though)
- [ ] NixPkgs packaging

See the [open issues](https://github.com/ri0t/mqttnotifier/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPLv3 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

riot - [@aufstand](https://bsky.app/profile/aufstand.bsky.social) - riot@c-base.org

Project Link: [https://github.com/ri0t/mqttnotifier](https://github.com/ri0t/mqttnotifier)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This project was started due to missing functionality and i heavily use it with:

* [Home Assistant](https://home-assistant.io)
* [Home Assistant - AVM Callmonitor Extension](https://www.home-assistant.io/integrations/fritzbox_callmonitor)

I use these three in combination to display popup notifications when someone's calling on the landline.
If you're envious now and want that as well, you can ask me about my automation scripts glueing everything together.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ri0t/mqttnotifier.svg?style=for-the-badge
[contributors-url]: https://github.com/ri0t/mqttnotifier/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ri0t/mqttnotifier.svg?style=for-the-badge
[forks-url]: https://github.com/ri0t/mqttnotifier/network/members
[stars-shield]: https://img.shields.io/github/stars/ri0t/mqttnotifier.svg?style=for-the-badge
[stars-url]: https://github.com/ri0t/mqttnotifier/stargazers
[issues-shield]: https://img.shields.io/github/issues/ri0t/mqttnotifier.svg?style=for-the-badge
[issues-url]: https://github.com/ri0t/mqttnotifier/issues
[license-shield]: https://img.shields.io/github/license/ri0t/mqttnotifier.svg?style=for-the-badge
[license-url]: https://github.com/ri0t/mqttnotifier/blob/master/LICENSE

[liberapay-shield]: https://img.shields.io/liberapay/gives/:riot
[liberapay-url]: https://liberapay.com/riot/
[patreon-shield]: https://img.shields.io/badge/-Patreon-black.svg?style=for-the-badge&logo=patreon&colorB=555
[patreon-url]: https://www.patreon.com/user?u=29020487
[screenshot]: images/screenshot.png
