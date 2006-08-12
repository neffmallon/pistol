background { rgb <1.000,1.000,1.000> }
camera{
 location <0.000,0.500,-5.000>
 look_at <0.000,0.000,0.000>
}
light_source{
 <30.000,30.000,30.000>
 color rgb <1.000,1.000,1.000>
}
plane{
 <0.000,1.000,0.000>,-1
texture{
pigment {
 checker
 rgb <1.000,1.000,1.000>,
 rgb <0.000,0.000,1.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
sky_sphere{
 pigment {
  gradient y
  color_map {
   [0.0 rgb <0.6,0.7,1.0>]
   [0.7 rgb <0.0,0.1,0.8>]
  }
 }
}
sphere{
 <0.000,0.000,0.000>,1.000
texture{
pigment {
 rgbt <0.800,0.800,1.000,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
reflection {
 0.80
 metallic
}
}
}
}
cylinder{
 <0.000,0.000,-2.000>, <1.000,1.000,-2.000>, 0.020
 open
texture{
pigment {
 rgbt <0.000,0.000,0.000,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
text {
 ttf "timrom.ttf" 
"Hi Rick" 1,<0.000,2.000,2.000>
}
