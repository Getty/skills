# Lifecycle and terminology

## Identify the layer

| Term | What it is | What it is not |
| --- | --- | --- |
| Native integration | Code included with HA for a device/service | A separately running server |
| Custom integration | Additional backend code loaded by HA | An isolated application sandbox |
| Dashboard card/theme | Browser presentation code/style | Device communication by itself |
| HAOS App, formerly add-on | Separately packaged service managed by Supervisor | A HACS repository type |
| Get HACS App | Initial downloader/bootstrap | HACS's ongoing runtime |
| External bridge | Separate service such as MQTT bridge | Automatically backed up with Container HA |

Classic HACS is an integration and does not manage HAOS Apps; Get HACS is a bootstrap exception. [HACS Apps FAQ](https://www.hacs.xyz/docs/faq/addons/). HACS distributes community elements whose support belongs to their projects, not automatically the HA core team. [HACS purpose](https://www.hacs.xyz/docs/faq/highlights/).

## Classic route: installed HA 2026.10 or older

Check the HACS prerequisites against the actual system. Choose the official download route for HAOS or Container; legacy documentation tabs do not make obsolete HA installation methods supported again. Read any installer before running it with filesystem access. [Prerequisites](https://www.hacs.xyz/docs/use/download/prerequisites/), [download](https://www.hacs.xyz/docs/use/download/download/).

After downloading and restarting HA, add the HACS integration and follow the documented GitHub authorization flow. Do not paste tokens into logs or a prompt. Then download the required repository and complete its own integration/resource configuration. [Initial configuration](https://www.hacs.xyz/docs/use/configuration/basic/).

Custom repositories require the correct repository URL, supported structure, and type. Adding a URL is not proof of compatibility. [Custom repositories](https://www.hacs.xyz/docs/faq/custom_repositories/).

## Forward-looking version gate

As of 2026-10-22, HACS's published guidance describes HA **2026.11** incorporating HACS as Settings → Marketplace. It describes migration of downloaded projects/custom repositories, old dashboard paths remaining compatible, and AppDaemon/Python-script files remaining while update management changes. Do not apply that procedure to 2026.10 or assume a future release is already installed. When the target release exists, recheck the official migration page and its release notes; never manually force both competing managers onto one instance. [Published Marketplace transition guidance](https://www.hacs.xyz/docs/marketplace/).
