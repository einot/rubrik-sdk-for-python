# Quick Start Guide: Rubrik SDK for Python (Rubrik Security Cloud)

## Authentication Mechanisms

The RSC SDK requires you to authenticate using your client credentials.

### Authenticate with Client Credentials

You can authenticate by providing the `domain` of your RSC account as well as the `client_id` and `client_secret` of your RSC service account. Here is a Python code example:

```python
from rubrik_security_cloud import RscClient

rsc_client = RscClient(
  domain='account.my.rubrik-lab.com',
  client_id='my_client_id',
  client_secret='my_client_secret',
)
```

### Using Environment Variables

Credentials can also be set through environment variables.

```sh
export RSC_CLIENT_ID='my_client_id'
export RSC_CLIENT_SECRET='my_client_secret'
export RSC_DOMAIN='account.my.rubrik-lab.com'
```

Then call the following

```python
import os
from rubrik_security_cloud import RscClient

rsc_client = RscClient()
```
