#!/bin/bash
@echo off 
echo "RELOPEC Test Started"

while :
do
    sudo ./libiec61850/relopec/sv_subscriber/sv_subscriber | python RELOPEC_algorithm.py || break;
done


