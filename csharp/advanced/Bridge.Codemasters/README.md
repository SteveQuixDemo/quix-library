# C# Bridge for Codemasters F1 2019
This bridge is capable of streaming the game's telemetry (PC or Console). 

**It is intended to be run on a pc on your local network and not deployed within Quix**

## Requirements / Prerequisites
 - Codemasters F1 2019 on PC or Console

## Environment Variables
- **Topic**: The topic where game data will be output
- **Token**: Bearer token to access Quix
- **FilePaths**: The folder where recorded data will be stored

## Run the sample
- Open Bridge.Codemasters.sln with your IDE
- Build
- Run Bridge.Codemasters.Console project inside IDE or run Bridge.Codemasters.Console.exe from the bin folder

## Content of the sample
- Bridge.Codemasters.sln: The solution file describing what projects to include
- Bridge.Codemasters.Console: The console application wiring up the code so it can transform incoming data and send it to quix. This is what you can configure via appsettings.json.
- Bridge.Codemasters.Quix: Contains logic to transform data objects to quix and send it to the platform.
- Bridge.Codemasters: Contains game specific logic for transforming the byte packets to usable data objects.


## Bridge.Codemasters.Console sppsettings.json
The application has two modes of running. 
- "udp": Set "Input" to "udp". This will listen to UDP packages on the network according to the "UDPInput" configuration.
- "file" Set "Input" to "file". This will replay one or more files specified under "FileInput" configuration.
More information can be found in Bridge.Codemasters.Console/Configuration/Config.cs.

## Docs
Check out the [SDK Docs](https://quix.ai/docs/sdk/introduction.html) for detailed usage guidance

## How to Run
Run this code locally a machine with access to the local network.
