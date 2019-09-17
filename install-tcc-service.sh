#!/bin/bash
cp tcc.service /etc/systemd/system/tcc.service
chmod 644 /etc/systemd/system/tcc.service
systemctl start tcc
systemctl enable tcc