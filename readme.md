<h1 align="center">
  <br>
  <img src="logo.svg" alt="school-utils" width="400">
  <br>
  <b>School Utils</b>
</h1>

<p align="center">
This repo is a collection of some tools that I built for school.
<br/>
Made by Jaiden.
</p>

# About

This is a collection of some tools that I built for school.

Featuring:

- A widget for Garmin watches that can collect how much money I have on my school card.
- A widget for Garmin watches that can tell me my next class and schedule.
- A status bar for MacOS that tells me how much money I have on my school card, my next class, and can be customized.

# To Install

Download or clone the repository via:

```bash
git clone https://github.com/JaidenAGrimminck/school-utils.git
```

# Status Bar

## Prerequesites

- Python >=`3.12`
- Using MacOS

Navigate to the repository and run:

```bash
python3 -m pip install -r requirements.txt
```

> *Note: You may also need to run...*
> ```bash
> python3 -m pip install datetime
> ```
> *...if you have any issues.*

## To Use

To run, run the following command:

```bash
python3 main.py
```


# Watch Face

## Prerequesites

- [Garmin SDK](https://developer.garmin.com/connect-iq/overview/) (follow the Getting Started tutorial)
- A Garmin watch

## To Build

First, open the `manifest.xml` and change the product / target device to your watch type.

Then, open the "watchface" folder and press CMD (or CTRL) + Shift + P, then find `Monkey C: Build for Device`, and run it.

## To Deploy

Plug in your watch to your computer, then navigate to the APPS folder within your watch. Drag and drop the `.[insert]` file, and remove your watch. It should be found by scrolling up/down on your watch!