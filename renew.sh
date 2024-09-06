#!/bin/bash

domain="numby.me"

remaining_days=$(certbot certificates -d $domain | grep "Expiry Date" | awk '{print $6}')

if [ $remaining_days -lt 30 ]; then
    echo "Renewing certificate for $domain..."
    certbot renew -d "$domain"
else
    echo "Certificate for $domain is valid for another $remaining_days days"
fi
