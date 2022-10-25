// Constants.
// Symbols as used in USGS PP 1395: Map Projections - A Working Manual
const DatumEqRad = [6378137.0,
    6378137.0,
    6378137.0,
    6378135.0,
    6378160.0,
    6378245.0,
    6378206.4,
    6378388.0,
    6378388.0,
    6378249.1,
    6378206.4,
    6377563.4,
    6377397.2,
    6377276.3]; 
const DatumFlat = [298.2572236,
   298.2572236,
   298.2572215,
   298.2597208,
   298.2497323,
   298.2997381,
   294.9786982,
   296.9993621,
   296.9993621,
   293.4660167,
   294.9786982,
   299.3247788,
   299.1527052,
   300.8021499]; 

const Item = 0;                    // default
const a    = DatumEqRad[Item];     // equatorial radius (meters)
const f    = 1 / DatumFlat[Item];  // polar flattening
const drad = Math.PI / 180;        // convert degrees to radians

// Mor constants, extracted from the function:
const k0   = 0.9996;                      // scale on central meridian
const b    = a*(1 - f);                   // polar axis
const e    = Math.sqrt(1 - (b/a)*(b/a));  // eccentricity
const e0   = e / Math.sqrt(1 - e*e);      // called e' in reference
const esq  = (1 - (b/a) * (b/a));         // e² for use in expansions
const e0sq = e*e / (1 - e*e);             // e0² — always even powers

function utmToLatLon(x, y, utmz, north) {

// First some validation:
if (x < 160000 || x > 840000) {
alert("Outside permissible range of easting values.");
return;
} 
if (y < 0){
alert("Negative values are not allowed for northing.");
return;
}
if (y > 10000000) {
alert("Northing may not exceed 10,000,000.");
return;
}

// Now the actual calculation:
const zcm = 3 + 6*(utmz-1) - 180;  // central meridian of zone
const e1  = (1 - Math.sqrt(1 - e*e)) / (1 + Math.sqrt(1 - e*e));  // called e₁ in USGS PP 1395
const M0  = 0;  // in case origin other than zero lat - not needed for standard UTM

let M;  // arc length along standard meridian
if (north) {
M = M0 + y/k0;
} else {  // southern hemisphere
M = M0 + (y-10000000) / k;
}
const mu = M / (a * (1 - esq*(1/4 + esq*(3/64 + 5*esq/256))));
let phi1 = mu + e1*(3/2 - 27*e1*e1/32)*Math.sin(2*mu) + e1*e1*(21/16 -55*e1*e1/32)*Math.sin(4*mu);  // footprint Latitude
phi1 = phi1 + e1*e1*e1*(Math.sin(6*mu)*151/96 + e1*Math.sin(8*mu)*1097/512);
const C1 = e0sq * Math.pow(Math.cos(phi1), 2);
const T1 = Math.pow(Math.tan(phi1), 2);
const N1 = a / Math.sqrt(1 - Math.pow(e * Math.sin(phi1), 2));
const R1 = N1 * (1 - e*e) / (1 - Math.pow(e * Math.sin(phi1), 2));
const D  = (x - 500000) / (N1*k0);
let phi = (D*D) * (1/2 - D*D * (5 + 3*T1 + 10*C1 - 4*C1*C1 - 9*e0sq) / 24);
phi = phi + Math.pow(D, 6) * (61 + 90*T1 + 298*C1 + 45*T1*T1 -252*e0sq - 3*C1*C1) / 720;
phi = phi1 - (N1 * Math.tan(phi1) / R1) * phi;

// Output Latitude:
const outLat = Math.floor(1000000*phi / drad) / 1000000;

const lng = D * (1 + D*D * ((-1 -2*T1 -C1)/6 + D*D * (5 - 2*C1 + 28*T1 - 3*C1*C1 + 8*e0sq + 24*T1*T1) / 120)) / Math.cos(phi1);
const lngd = zcm + lng/drad;

// Output Longitude:
const outLon = Math.floor(1000000*lngd)/1000000;

return [outLat, outLon];
}