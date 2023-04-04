# Remote virus protection (RVP)

## Motivation

The reason I developed the RVP service is to enhance the security of my build server. As a developer, I often rely on numerous open-source packages such as Node.js and NuGet packages, which can potentially contain malware or viruses that may infect my final product. Therefore, to reduce this risk, I decided to implement a solution that would enable me to scan every build result using different virus scanners, ensuring that no malware or viruses would make it into my end product through my build results.

While considering different antivirus options, I quickly realized that installing a virus scanner on my build server would significantly impact the speed of my build agent. As a result, I decided to use a remote scanner and developed the RVP service, which has proven to be a reliable and essential component of my build process and continuous integration process. With the RVP service, I can now scan all my build results with different virus scanners, thus ensuring the highest level of security for my final product.

In addition to the increased security, the RVP service is also super easy to use and implement in other solutions over HTTP interface. Therefore, other developers can also benefit from this microservice, which provides an additional layer of protection to their solution or build process without compromising on the speed or efficiency.

## Support of scanners

RVP supports a variety of virus scanners, including popular open-source options like ClamAV and Windows Defender, as well as paid premium scanners. This flexibility allows users to choose the scanner that best fits their needs or already in action. 

Currently, the following scanners are functional (and the list is expanding):

**Windows-Enviorments**:
* Windows Defender

**Linux-Enviorments**:
* ClamAV
* ESET Server Security for Linux

## Start the service

Please check the _.env_-file for configuration and pay attention to the [pitfalls](#Pitfalls) section.

```bash
python server.py
```

Check if the service is running on http://localhost:8080.
## How to use

### Use with curl

You can either obtain an infected test file for your machine or use a non-infected file.

```bash
wget https://secure.eicar.org/eicar_com.zip
```

To upload your file to the RVP service, you must use the HTTP-PUT method and specify the port number provided in the _.env_-file that the service is listening on.

```bash
curl http://127.0.0.1:8080 --upload-file eicar_com.zip --http0.9
```

The result of this endpoint is the file hash of the uploaded file, accompanied by an HTTP status code of 200 (OK). For example: 6ce6f415d8475545be5ba114f208b0ff.

To get the result of a scan use the /resultof/{filehash} endpoint.
```bash
curl -v http://127.0.0.1:8080/resultof/6ce6f415d8475545be5ba114f208b0ff --http0.9
```

Multiple responses are possible:
* 102 (Processing): The scan is not done yet, please retry again in a few seconds.
* 200 (OK): The scan is complete and no threats were found.
* 406 (Not Acceptable): The scan is complete threats were found.
* 500 (Internal Server Error): The scan is complete threats were found.

A JSON response is provided for HTTP status codes 200, 406, and 500.
```json
{
  "returncode": "INFECTED", // OK, INFECTED or FISHY
  "threats": ["Virus:DOS/EICAR_Test_File"], // ALL THREATS
  "log": "", // LOG OF THE SCANNER
  "filehash": "6ce6f415d8475545be5ba114f208b0ff" // FILEHASH
}
```

### RVP client.py
```bash
python client.py http://0.0.0.0:8080 Test.zip 
```

## Example implementation of RVP in an Azure Build Pipeline
> TODO

## Pitfalls

### Real-time scans

You should enter exceptions for all virus scanners that perform real-time scanning. Otherwise the file will be removed by many virus scanners during the upload and RVP will not be able to perform its scans.

#### Windows Defender
In Windows environments, you can execute the following PowerShell command to exclude the path for Windows Defender.

```powershell
powershell -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath "C:\pathToRVP\storage\__vault"
```

### Multiple scanners in one environment
Installing multiple virus scanners on the same system is not recommended as it can result in conflicts and performance issues. It is advisable to install a single scanner on each system or Docker container.

# Contributions

I would greatly appreciate your help in enhancing the service's functionality. Additionally, if you use different virus scanners, it would be great if you could also contribute by adding them to the service.

# License

RVP is open source and released under the MIT license.

# Credits
Special thanks for the contribution goes to
* [steffendx](https://github.com/steffendx)
* [DEV-Team of linqi.de](https://linqi.de)

![www/assets/rvp_logo.svg](www/assets/rvp_logo.svg | width=250)