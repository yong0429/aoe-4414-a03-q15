# ecef_to_llh.py
#
# Usage: python3 ecef_to_llh.py r_x_km r_y_km r_z_km
#  Converts ECEF vector components to LLH
#  See "Fundamentals of Astrodynamics and Applications, Fourth Edition" by
#  David A. Vallado, pages 172-173
# Parameters:
#  r_x_km: ECEF x-component in km
#  r_y_km: ECEF y-component in km
#  r_z_km: ECEF z-component in km
# Output:
#  Prints the converged latitude (deg), longitude (deg), and HAE (km)
#
# Written by Brad Denby
# Other contributors: Yonghwa Kim
#
# This work is licensed under CC BY-SA 4.0

# import Python modules
import math # math module
import sys  # argv

# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456

# helper functions

## calculated denominator
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

# initialize script arguments
r_x_km = float('nan') # ECEF x-component in km
r_y_km = float('nan') # ECEF y-component in km
r_z_km = float('nan') # ECEF z-component in km

# parse script arguments
if len(sys.argv)==4:
  r_x_km = float(sys.argv[1])
  r_y_km = float(sys.argv[2])
  r_z_km = float(sys.argv[3])
else:
  print(\
   'Usage: '\
   'python3 ecef_to_llh.py r_x_km r_y_km r_z_km'\
  )
  exit()

# write script below this line

# calculate longitude
lon_rad = math.atan2(r_y_km,r_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(r_z_km/math.sqrt(r_x_km**2+r_y_km**2+r_z_km**2))
r_lon_km = math.sqrt(r_x_km**2+r_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((r_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E

# print latitude (deg), longitude (deg), and HAE (km)
print(lon_deg)
print(lat_rad*180.0/math.pi)
print(hae_km)