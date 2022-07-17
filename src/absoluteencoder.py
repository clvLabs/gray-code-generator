import math
import svgwrite

from . import styles

class AbsoluteEncoder:

  def __init__(self, args):
    self.args = args
    self.dwg = svgwrite.Drawing(self.args.outfile, debug=True)
    self._generate()


  def save(self):
    if not self.args.quiet:
      print(f"Saving {self.args.bits} bit encoder as {self.args.outfile}")

    self.dwg.save()


  def _generate(self):
    if not self.args.quiet:
      print(f"Generating {self.args.bits} bit encoder ({2**self.args.bits - 1} pieces)")

    for bit in range(self.args.bits-1, -1, -1):
      self._draw_bit(bit)


  def _get_bit_pos(self, bit):
    return self.args.bits - 1 - bit


  def _get_pos_bit(self, pos):
    return self.args.bits - 1 - pos


  def _get_bit_arc_span(self, bit):
    bit_pos = self._get_bit_pos(bit)

    if bit_pos <= 1:
      return (math.pi/2)
    else:
      return (1 / 2**(bit_pos-1)) * (math.pi/2)


  def _get_bit_start_angle(self, bit):
    bit_pos = self._get_bit_pos(bit)
    _angle = math.pi
    for i in range(bit_pos):
      if i == 0:
        _angle += self._get_bit_arc_span(self._get_pos_bit(i))
      else:
        _angle += self._get_bit_arc_span(self._get_pos_bit(i)) / 2

    return _angle


  def _draw_bit(self, bit):
    bit_pos = self._get_bit_pos(bit)

    _bits = self.args.bits
    _id = self.args.inner_diameter
    _od = self.args.outer_diameter

    _center = (_od / 2, _od / 2)
    _usable_diameter = _od - _id
    _usable_radius = _usable_diameter / 2
    _bit_height = _usable_radius / _bits

    _radius_in = _id / 2
    _radius_in += bit_pos * _bit_height
    _radius_max = _radius_in + _bit_height
    _radius_out = _radius_max - self.args.gap

    if not self.args.quiet:
      print(f"[Draw] bit: {bit} - arcspan: {self._get_bit_arc_span(bit):7.5f} - pieces: {2**bit_pos}")

    if self.args.debug:
      # LIMIT CIRCLES
      self.dwg.add(self.dwg.circle(_center, _radius_in, **styles.DEBUG_LIMIT))
      self.dwg.add(self.dwg.circle(_center, _radius_out, **styles.DEBUG_LIMIT))
      self.dwg.add(self.dwg.circle(_center, _radius_max, **styles.DEBUG_LIMIT))

    if bit_pos <= 1:
      num_pieces = 1
    else:
      num_pieces = 2**(bit_pos-1)

    for piece_num in range(num_pieces):
      self._draw_piece(bit, piece_num)


  def _draw_piece(self, bit, piece_num):
    bit_pos = self._get_bit_pos(bit)

    _bits = self.args.bits
    _id = self.args.inner_diameter
    _od = self.args.outer_diameter

    _center = (_od / 2, _od / 2)
    _usable_diameter = _od - _id
    _usable_radius = _usable_diameter / 2
    _bit_height = _usable_radius / _bits

    _radius_in = _id / 2
    _radius_in += bit_pos * _bit_height
    _radius_max = _radius_in + _bit_height
    _radius_out = _radius_max - self.args.gap

    _angle1 = self._get_bit_start_angle(bit)
    _angle1 += self._get_bit_arc_span(bit) * (piece_num*4)
    _angle2 = _angle1 - self._get_bit_arc_span(bit)*2

    def _calcpos(radius, angle):
      _xpos = _center[0] + radius * math.cos(angle)
      _ypos = _center[1] + radius * math.sin(angle)
      return (_xpos, _ypos)

    _pos1 = _calcpos(_radius_in, _angle1)
    _pos2 = _calcpos(_radius_out, _angle1)
    _pos3 = _calcpos(_radius_out, _angle2)
    _pos4 = _calcpos(_radius_in, _angle2)


    if self.args.debug:
      styles.ARC['stroke_width'] = 0.5

    _path = svgwrite.path.Path(
      f"M {_pos1[0]} {_pos1[1]}",
      **styles.ARC,
      )


    if self.args.debug:
      # BASE LINE
      self.dwg.add(self.dwg.line(_center, _pos1, **styles.DEBUG_LINE))
      self.dwg.add(self.dwg.line(_center, _pos3, **styles.DEBUG_LINE))

      # POS CIRCLES
      self.dwg.add(self.dwg.circle(_pos1, 1, **styles.DEBUG_POS))
      self.dwg.add(self.dwg.circle(_pos2, 1, **styles.DEBUG_POS))
      self.dwg.add(self.dwg.circle(_pos3, 1, **styles.DEBUG_POS))
      self.dwg.add(self.dwg.circle(_pos4, 1, **styles.DEBUG_POS))

      self.dwg.add(self.dwg.circle(_center, 1, **styles.DEBUG_POS))


    _path.push_arc(
      target=_pos2,
      rotation=0.0,
      r=_od*10,
      large_arc=False,
      angle_dir="-",
      absolute=True,
    )

    _path.push_arc(
      target=_pos3,
      rotation=0.0,
      r=_radius_out,
      large_arc=False,
      angle_dir="-",
      absolute=True,
    )

    _path.push_arc(
      target=_pos4,
      rotation=0.0,
      r=_od*10,
      large_arc=False,
      angle_dir="-",
      absolute=True,
    )

    _path.push_arc(
      target=_pos1,
      rotation=0.0,
      r=_radius_in,
      large_arc=False,
      angle_dir="+",
      absolute=True,
    )

    self.dwg.add(_path)
