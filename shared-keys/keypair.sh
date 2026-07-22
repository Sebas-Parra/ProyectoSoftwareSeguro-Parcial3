#!/usr/bin/env bash

openssl genpkey -algorithm RSA -out shared-keys/private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in shared-keys/private.pem -outform PEM -pubout -out shared-keys/public.pem