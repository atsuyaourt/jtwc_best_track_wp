# JTWC Western North Pacific Best Track Data

Information about the data can be found [here](https://www.metoc.navy.mil/jtwc/jtwc.html?western-pacific)

Period: 1945 - 2022

**Columns extracted:**

- _CY_ - Annual cyclone number
- _Year, Month, Day, Hour_ - Warning date
- _Lat, Lon_ center location
- _VMax_ - Maximum sustained wind speed in knots: 0 - 300
- _MSLP_ - Minimum sea level pressure, 1 - 1100 MB

**Derived columns:**

- _SN_ - Serial number: _YYYYCY_
- _Cat_ - Tropical Cyclone category based on the [_Saffir-Simpson_ scale](https://www.nhc.noaa.gov/aboutsshws.php)
