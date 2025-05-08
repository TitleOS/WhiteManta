# White Manta - A web monitoring page for EFF's RayHunter

## What is WhiteManta?
WhiteManta is a Python Flask script packaged into a Dockerimage that is designed to relay information from a rooted hotspot device such as the Orbic RC400L, running EFF's [Rayhunter](http://github.com/EFForg/rayhunter) stingray detection software. Normally you can only access Rayhunter's reports by either connecting to the hotspot's local WiFI network or via ADB port forwarding over USB. This container aims to remove that restriction by allowing you to connect your hotspot via USB to one device running the container, which will then host a web page accessible by any device on your network. 

In addtion, White Manta can be configured to hit a WebHook of your choice any time a stingray interception device is active, allowing you to get anything from a Push Notification, to SMS text or email. 

## Features
* Easy installation, simply connect your Orbic installed with Rayhunter to the PC that will be running the White Manta container over USB-C, before running `adb forward 14480:tcp 80:tcp` which will allow the White Manta container to query the web page running on the Orbic via TCP port 14480.

* Webhook Trigger when Stingray is detected allowing for various means of notification.

* Monitor resource usage of hotspot hardware

* Access Rayhunter information remotely

## Installation (WIP)
Build Docker image.

Map container port 8888 to desired port on host machine to view WhiteManta's Web UI.

Set enviroment variable "webhook_url" to webhook target.

Deploy container.

