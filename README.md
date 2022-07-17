# gray-code-generator

Generate customizable absolute position radial Gray code encoders in `svg` format.

## Samples

8 bit encoder:
```
$ ./generate-encoder.py 8 test.svg
```
<img src="docs/resources/images/sample.svg" width="500" height="500"/>

3/5/7/9 bit encoders:

<img src="docs/resources/images/3-bit.svg" width="200" height="200"/>
<img src="docs/resources/images/5-bit.svg" width="200" height="200"/>
<img src="docs/resources/images/7-bit.svg" width="200" height="200"/>
<img src="docs/resources/images/9-bit.svg" width="200" height="200"/>


## Setup
Before using you must install [svgwrite](https://pypi.org/project/svgwrite/):

```
$ pip install svgwrite
```

## Usage

```
$ ./generate-encoder.py -h
usage: generate-encoder.py [-h] [-g GAP] [-id INNER_DIAMETER] [-od OUTER_DIAMETER] [-d] [-q] bits outfile

positional arguments:
  bits                  number of bits
  outfile               name of the generated SVG

optional arguments:
  -h, --help            show this help message and exit
  -id INNER_DIAMETER, --inner-diameter INNER_DIAMETER
                        diameter of the inner circle
  -od OUTER_DIAMETER, --outer-diameter OUTER_DIAMETER
                        diameter of the outer circle
  -g GAP, --gap GAP     gap between bits
  -d, --debug           debug mode (adds extra figures to output)
  -q, --quiet           suppress console output
```

## Size units
Please note there is no unit (`cm`/`mm`/`inches`/etc) or `dpi` associated to the generated `svg` file. All values are expressed in _points_.

To match exact sizes in the real world either manually resize the shape in your editor of choice or calculate the equivalent _points_ for the size(s) and `dpi` you need.

### Calculation examples
For a 10cm `outer-diameter` @ 300`dpi` you have to specify `-od 1181`:
```
( 10 / 2.54 ) * 300 = 1181
```

For a 2.5 inch `outer-diameter` @ 300`dpi` you have to specify `-od 750`:
```
2.5 * 300 = 750
```

## Inner and outer diameters
To create an encoder with specific dimensions/proportions, use the `-od` and `-id` parameters.

For an encoder with an `outer-diameter` of 4 inches and an `inner-diameter` of 3 inches @ 300`dpi`:

```
$ ./generate-encoder.py 10 test.svg -od 1200 -id 900
```
<img src="docs/resources/images/id-od.svg" width="200" height="200"/>


## Leaving gaps between bits

If you specify a `--gap`, the specified size will be substracted from the _top_ (the outer edge) of each bit.

The `inner-diameter` will be respected, but keep in mind that the outer `gap` radius will be empty, as it will be the gap of the last bit.

<img src="docs/resources/images/gap-1.svg" width="200" height="200"/>

With bigger `gaps` you can have bits' _arc pieces_ represented as thin lines:

<img src="docs/resources/images/gap-2.svg" width="200" height="200"/>

Negative gaps can also be used to make sure the _pieces_ do overlap:

<img src="docs/resources/images/gap-3.svg" width="200" height="200"/>


## Making an encoder from a single line

In some cases (e.g. when 3D-extruding or laser cutting) it may be important to generate the shape as a single closed path.

The recommended procedure in these cases is:
* Use `--gap -0.1` to make sure your _pieces_ overlap
* Use any vector image editor (such as [Inkscape](https://inkscape.org/)) to open the `svg` file:
  * Ungroup the _pieces_.
  * Apply a [boolean union](https://inkscape-manuals.readthedocs.io/en/latest/boolean-operations.html?highlight=union#boolean-operations) to the individual _pieces_ so they become one.

## Debug mode

Using the `-d` option will add some extra shapes identifying the anchors and baselines used to construct the encoder. It was created to help while developing, but I found it nice and kept it :)

<img src="docs/resources/images/debug.svg" width="200" height="200"/>
