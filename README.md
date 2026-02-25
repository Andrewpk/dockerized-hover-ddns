# Dockerized Hover Dynamic DNS

This is a dockerized version of the project [hover-dyn-dns](https://github.com/pjslauta/hover-dyn-dns).

Many thanks to the developer in having the hover private API documented.

## Usage
For detailed usage, refer to the original project's config.json file.

At a minimum, the container will need these environment variables set:
```
ENV HOVER_USERNAME="" # Your Hover username
ENV HOVER_PASSWORD="" # Your Hover password
ENV HOVER_TOTP_SECRET="" # Your Hover TOTP secret
ENV HOVER_DNS_ID="" # The dnsID for the record you want to update. This can be a base domain or a subdomain.
ENV HOVER_ROOT_DOMAIN="" # The base domain for the record you want to update, e.g. "example.com"
```

### TOTP Secret
If you have no way to view your current 2fa TOTP secret, you can disable your current 2fa, and then note the "seed" 
TOTP secret when you reactivate it.

### The Basics
First you'll need to get the hover dnsID for the domain you want to update. 

By running the container with the environment variable `HOVER_GET_DNSIDS=true` set, the container will print out all 
the dnsIDs for the domains in your Hover account and then exit.

Once you have the correct dnsID, you can set the `HOVER_DNS_ID` environment variable to that value and run the 
container. It will then update the IP address for that record every 5 minutes by default.

If you want to change the run interval, the `HOVER_RUN_INTERVAL` is there for you! Set the value to the number of 
seconds you want between runs.


