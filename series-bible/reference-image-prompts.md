# Reference Image Pack: Default Setting (working title)

Generate these first. Pick one winner per character and use it as the image reference (image-to-video) for every clip so Dan and the Figure stay consistent.

## Global style (paste at the end of every prompt)

Cinematic thriller look, photorealistic, 35mm lens, shallow depth of field, fine film grain, 9:16 vertical, no text, no logos, no brand names.
Palette: cold desaturated slate-blue (tension), warm natural gold (clarity). Never both at full strength in one frame.

## 1. Dan (hero)

Lock description (reuse verbatim in every prompt):
"Dan, a fit 48-year-old man, lean athletic build, short salt-and-pepper hair, light stubble, tired but alert hazel eyes, charcoal quarter-zip athletic top"

- **1a Front, neutral:** Dan standing straight, facing camera, neutral expression, soft window light, plain light-gray wall, waist-up.
- **1b Three-quarter, tense:** Dan three-quarter view, jaw tight, anxious eyes, cold blue dawn side-light, bathroom background.
- **1c Profile, calm:** Dan in profile, calm and relieved, warm golden morning sun on his face, outdoors.
- **1d Full body:** Dan full-length, walking, relaxed posture, athletic pants and the same top, neutral street.

## 2. The Figure (antagonist)

Lock description:
"a tall, faceless silhouette in matte black, human-shaped, soft blurred edges, no facial features, no visible clothing detail, always slightly out of focus"

- **2a Doorway:** the Figure standing in a dim bathroom doorway, cold blue light, out of focus, Dan's back in the foreground.
- **2b Glass:** the Figure behind frosted office glass, partly reflected, fluorescent light.
- **2c Rearview:** the Figure seated in the back seat of a parked car, visible only in the rearview mirror.
- **2d Far end of aisle:** the Figure at the far end of a long grocery aisle, small in frame, straightening a display.

## 3. Locations (empty, no people)

- **3a Bathroom:** minimalist bathroom, tempered-glass digital scale on the floor, red LED display glowing, cold dawn light.
- **3b Kitchen:** modern kitchen, black coffee pouring into a mug, untouched healthy breakfast plate pushed aside, side-lit and moody.
- **3c Car interior:** parked car, empty driver's seat, steering wheel, hazy morning glare through the windshield.
- **3d Office:** open-plan office, cold fluorescent light, an unmarked pink bakery box on a desk.
- **3e Grocery aisle:** long supermarket aisle, a cereal box with a generic invented label glowing at eye level, snack pyramid at the aisle end.
- **3f Coastal path:** sunlit coastal park trail under trees, golden hour (the "resolution" location).

## 4. Motif plates

- **4a Heartbeat:** macro of a glass of water, droplets condensing, a faint pulse ripple on the surface, cold blue.
- **4b Mirror:** a bathroom mirror reflecting an empty room with the Figure faintly visible (series twist plant).

## Workflow

1. Generate 4 variations of each, pick 1 winner for Dan (1a-1d) and 1 for the Figure.
2. Save winners as `dan_ref_*.png` and `figure_ref_*.png`.
3. Feed them as image references to the video model for every shot.
4. Keep the lock descriptions word-for-word in each prompt.
