#!/usr/bin/python3
import json

s = '''{
	"data": 
	{
		"code": ["<span class="imgval" style="width:5px;"><div class="imgtxt" style="margin-left:-0px;"></div></span><span class="imgval" style="width:3px;"><div class="imgtxt" style="margin-left:-45px;"></div></span><style>.imgval .imgtxt{background:url("/Interface/IndexShow/img/?res=M1ogAzwPACQvRyQHFnNjFzxCRyweYDEMIhYwCh0eV14WDRdVJA9xCHJvLn0DDHUNZ0wudj4TR1UNABdRIhBdZFgVJRw2XhtXEzUdBBRrLCE7cyswLyFkOGIUZjZ6CF4BQBsjJFIHdjE8Oy5xIDQkQkVaLwdYLCZRHDkXIVxrGXclCXxnIhIdFAYUNWRYdHA6KxMZaDIidiEwOCR9K1ZMGi4JBThZFUZkA1sHBxoyZgNVBhECZFkBUVVQMSQkXn5bKToHFDknRSphMCALdAwAGjoHHiUgOB1pHhFBKg%3D%3D&res2=ZrEXSTR6.284414.8233K0Wuhlk9sE1XqeXkMCiGhcTxDJTSdqzzBinYFMxaEbTxjWZ14Zr&res3=a29WHzU0EX0AEXp9Z0twTmdGRgdEBANFU1tWB3cKAmV/cFEsXGNEHj8mcwcJFGtzbl0AZnN1Ah1kIAsALwMPYHl3SlIXdS9hZAJ1f0MkZgtwQVBSIGQGeHUXcF16PENyZ3ZQBHISdldCX0ZQRWMda1ZxcityBRB2YkBxDHNmClBECxstRCN2WDdQYXoVDm1+Q1QLO1M2dD5lQQZAHXgAZkAGVmZwIB11LTBGEw==&type=1")}</style>"]
	},
	"status": "0"',
	"message": ""
}'''

print(json.loads(s))