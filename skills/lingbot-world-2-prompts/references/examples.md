# Production examples (verbatim from LingBot-World 2 export data)

Five complete sessions from the model team's inference exports. Base prompts
and addenda are untouched. Sessions 2–5 are from the July 2026 export batch
(the current format: `f`, `g`, numbered event keys, optional `space` with
the "current controllable subject" jump string). Session 1 is an earlier
June export kept to show the playable-character base template and the legacy
fixed `u`/`o` slot layout.

On language: the Chinese numbered-key addenda below are the lab operators'
hand-typed working language, not a format requirement — the pipeline-generated
`f`/`g`/`space` addenda in the very same sessions are English. The bracketed
*[gloss: …]* translations are added here for reference and are **not** part
of the export. Our own deliverables are written in English (see SKILL.md);
these sessions are kept verbatim because they are the ground truth for the
key *structure* — event shapes, chaining, hand-offs — which is language-
independent.


## 1. Playable character — cigarette pack (legacy `u`/`o` layout)

The base template here is still current — the newest exports reuse it word
for word with a different subject. The action layout (`f/g/u/o/space` with
the old jump string) is the legacy format.

**Base prompt:**

> A third-person gameplay video where a cigarette pack is the playable character. The camera follows from behind and slightly above, like a modern 3D game. The cigarette pack smoothly slides across the ground in response to keyboard arrow keys (or WASD), changing direction naturally with game-like movement and physics. It always stays upright while sliding. The scene looks like real gameplay with realistic lighting, smooth camera tracking, high-quality graphics, and an Unreal Engine 5 style.

**Actions:**

- `f` **Slide And Stop** — The cigarette pack continues its smooth glide, sliding into the discarded cigarette filter resting on the ground. The impact nudges the filter, causing it to tumble and roll a short distance before coming to a rest beside the pack.
- `g` **Frosted Subway Floor** — A light layer of frost spreads across the dark, speckled subway floor, covering the cigarette pack and the filter in a crisp, icy sheen. The air grows visibly cold, with faint wisps of breath hanging in the dim station light, transforming the bustling commute into a quiet, wintry moment.
- `u` **Cigarette Slam** — The cigarette pack suddenly drops its forward momentum and slams its side onto a discarded cigarette butt, shattering the smaller cigarette into ash and filter pieces upon impact.
- `o` **Fires Cigarette** — The cigarette pack abruptly stops its slide and tilts forward, firing a small, glowing ember projectile from its lit end. The projectile streaks through the air with a faint trail of smoke, striking a nearby sneaker with a small puff of dust and leaving a tiny scorch mark on the fabric.
- `space` **Jump** — The character jumps high into the air.


## 2. Orbit — snowboarder on a sand dune (numbered keys, subject transformation)

Note the current orbit skeleton: "remains at the exact centre … orbiting
around the stable snowboarder only while held. With no event key pressed,
[idle pose]." Key 1 is a single beat, Key 2 adds a scene element, Key 3 is a
subject transformation that settles into a new stable state.

**Base prompt:**

> This is a third-person-view video of a hooded figure snowboarding down a vast sand dune. Cinematic rendering style. The snowboarder remains at the exact centre of the frame at constant size and distance. Neither the snowboarder nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting around the stable snowboarder only while held. With no event key pressed, the snowboarder stands balanced on the board, arms relaxed at their sides, ready to carve.

**Actions:**

- `f` **Fluttering Moths** — The original focal subject remains the main subject, unchanged in pose and position, while a swarm of luminous moths flutters into view from the dune's crest, casting delicate, shifting shadows across the figure's grey robes as they trace shimmering, undulating paths through the still air.
- `g` **Shifting Dunes** — The vast dune landscape shifts as if sculpted by an invisible wind, the sand ripples sharpening into stark, rhythmic ridges that march forward while the sky bleeds into a twilight palette of deep indigo and soft amber.
- `1` **Key 1** — 滑沙板突然疯狂加速向前冲，脚下爆发明亮的金色光芒，身后拖出一条发光的沙尘尾迹和更深的滑痕。 *[gloss: The sandboard suddenly rockets forward, bright golden light bursting beneath it, dragging a glowing dust trail and deeper carve marks behind.]*
- `2` **Key 2** — 前方沙地出现一条发光的蓝色水面倒影，像海市蜃楼一样铺在沙丘之间。 *[gloss: A glowing blue watery reflection appears on the sand ahead, spread between the dunes like a mirage.]*
- `3` **Key 3** — 滑沙板变成童话中的魔毯，穿灰色连帽衫的人站在魔毯上飞上天空，在沙丘上方平稳飘行。 *[gloss: The sandboard becomes a fairy-tale magic carpet; the grey-hooded figure rises into the sky standing on it, gliding steadily above the dunes.]*


## 3. First-person anchor — rally car cockpit (toggle `f`/`g`)

The anchor is the wheel and dashboard; `f`/`g` are a minimal toggle pair
(headlights on / wipers sweeping), each a single short Chinese sentence used
as both label and addendum. Note the current `space` string.

**Base prompt:**

> This is a first-person-view video from the driver's position inside a rally car cockpit. Gritty realism atmosphere. The steering wheel and dashboard remain at the exact centre of the frame at constant size and distance. Neither the steering wheel nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting around the stable vehicle interior only while held. With no event key pressed, the driver's gloved hands stay relaxed on the wheel, ready to steer or shift gears.

**Actions:**

- `f` **车灯亮了** — 车灯亮了 *[gloss: The headlights turn on]*
- `g` **雨刮器摆动** — 雨刮器摆动 *[gloss: The wipers sweep]*
- `space` **Jump** — The current controllable subject springs upward into the air.


## 4. First-person anchor — hospital corridor (chained escalation keys)

The anchor is the flashlight beam. Keys 1–5 are a designed chain: each
addendum opens by resolving the previous key's creature (it fades, dissolves,
retreats) before introducing the next one, so the keys read correctly when
pressed in order.

**Base prompt:**

> This is a first-person-view video from the operator's position holding a flashlight in a dilapidated hospital corridor. Gritty survival atmosphere. The flashlight beam remains at the exact centre of the frame at constant size and distance. Neither the flashlight nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting around the stable light source only while held. With no event key pressed, the gloved hands stay steady and relaxed, keeping the beam fixed on the peeling walls and abandoned gurneys ahead.

**Actions:**

- `f` **主人公的手电筒开着。** — 主人公的手电筒开着。 *[gloss: The protagonist's flashlight is on.]*
- `g` **主人公的手电筒关上。** — 主人公的手电筒关上。 *[gloss: The protagonist's flashlight is off.]*
- `1` **Key 1** — 病房门里伸出一只苍白腐烂的手，一个僵尸病人拖着僵硬身体缓慢走出门口，头低垂着，肩膀抽动，脚步沉重，地面传来湿冷拖行声。 *[gloss: A pale, rotting hand reaches out of a ward door; a zombie patient drags its stiff body slowly out, head hanging low, shoulders twitching, heavy footsteps and a wet scraping sound on the floor.]*
- `2` **Key 2** — 僵尸病人在门口停留片刻后，身体被黑暗吞没，逐渐消失。病房门无声打开，门内站着一名苍白吸血鬼，穿着破旧黑色礼服，脸隐藏在阴影中，只露出冰冷眼神和尖牙。门后的黑暗像浓雾一样向走廊缓慢蔓延。 *[gloss: After lingering at the door, the zombie is swallowed by darkness and fades away. The ward door swings open silently; inside stands a pale vampire in a ragged black suit, face hidden in shadow except for cold eyes and fangs. The darkness behind the door spreads slowly into the corridor like thick fog.]*
- `3` **Key 3** — 吸血鬼静静凝视一段时间后，化成黑雾消散在门内。走廊尽头的铁门剧烈震动，门缝中传出低沉吼声。一个高大怪兽从门里挤出，肩膀撞歪门框，爪子刮过墙面，墙皮和灰尘大片掉落，只能看到巨大的头部和起伏呼吸。 *[gloss: After staring silently, the vampire dissolves into black mist inside the doorway. The iron door at the corridor's end shakes violently, a low roar coming through the gap. A huge monster squeezes out, its shoulder knocking the doorframe askew, claws raking the wall, plaster and dust falling in sheets; only its massive head and heaving breath are visible.]*
- `4` **Key 4** — 高大怪兽咆哮片刻后，轮廓被烟尘覆盖，慢慢消失。门内传来沉重喘息，一个狼人般的畸形怪物蹲在病房地面，背部剧烈起伏，利爪抓着破旧床架。它猛地抬头，双眼反光，门框被它的身体挤得吱呀作响。 *[gloss: After roaring for a moment, the huge monster's outline is covered in dust and slowly vanishes. Heavy panting comes from inside; a werewolf-like deformed creature crouches on the ward floor, back heaving violently, claws gripping a battered bed frame. It snaps its head up, eyes reflecting light, the doorframe creaking as its body presses against it.]*
- `5` **Key 5** — 狼人般的畸形怪物低吼一段时间后，向后退入阴影，逐渐消失。前方路中间突然出现一个穿破旧戏服的小丑，歪着头站在门边，手里拿着红色气球，脸上的笑容僵硬夸张。灯光闪烁时，小丑的位置不断变化，时而在门口，时而出现在更近的病床旁。它停留片刻后，红色气球先爆裂，小丑随即消失在闪烁灯光中。 *[gloss: After growling for a while, the werewolf-like creature retreats into the shadows and fades. A clown in a ragged costume suddenly appears in the middle of the corridor, head tilted, holding a red balloon, its smile stiff and exaggerated. As the lights flicker, the clown's position keeps changing — now in the doorway, now beside a nearer bed. After a moment, the red balloon bursts first, and the clown vanishes into the flickering light.]*
- `space` **Jump** — The current controllable subject springs upward into the air.


## 5. First-person vista — Great Wall world tour (chained teleport keys)

A landmark as the anchor. Keys 1–7 are chained scene teleports: each names a
transition device (mist, lake haze, city lights, sunset glow) before
establishing the new location, and the last key explicitly closes the
journey. Note the `f`/`g` addenda here re-open with the full centre-lock
sentence — a pattern in some newer exports that the model tolerates but that
adds nothing; the skill doesn't imitate it. (This export also still carries
the older jump string.)

**Base prompt:**

> This is a first-person-view video of a sweeping vista along the Great Wall of China, with the ancient stone rampart and watchtowers winding across lush green mountain ridges. Crisp storybook rendering style. The stone wall remains at the exact centre of the frame at constant size and distance. Neither the wall nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting around the stable wall only while held. With no event key pressed, the scene remains still and static, presenting the enduring architecture against the rolling hills.

**Actions:**

- `f` **Forest Fox Appears** — The original focal subject remains the main subject, unchanged in pose and position, while the ancient stone rampart remains at the exact centre of the frame at constant size and distance, while a vibrant red fox darts across the sunlit grassy ridge nearby, its bushy tail twitching as it pauses to watch the distant watchtowers.
- `g` **Winter Snowscape** — The ancient stone rampart remains at the exact centre of the frame at constant size and distance, now winding across silent white mountain ridges instead of lush green foliage, with snow dusting the watchtowers and blanketing the foreground terrain.
- `1` **Key 1** — 画面被薄雾覆盖，雾散后到达埃及金字塔前。第一人称视角踩过金色沙地，仰望巨大的石块结构，远处骆驼队缓慢经过，阳光让沙漠泛起炽热光芒。 *[gloss: Thin mist covers the frame; as it clears, the view arrives before the Pyramids of Egypt. The first-person view steps over golden sand, looking up at the massive stone structures, a camel caravan passing slowly in the distance, sunlight setting the desert ablaze.]*
- `2` **Key 2** — 云雾逐渐化为湖面薄雾，场景转到杭州西湖。第一人称沿着湖边石板路前行，湖水清澈平静，远处是断桥、亭台和层叠青山，柳枝随风轻摆，水面倒映着天空和古典建筑。 *[gloss: The mist becomes lake haze and the scene shifts to West Lake, Hangzhou. The first-person view walks a lakeside stone path; the water is clear and calm, with the Broken Bridge, pavilions, and layered green hills in the distance, willow branches swaying, the lake mirroring sky and classical buildings.]*
- `3` **Key 3** — 视角继续前进，水面反光变成城市灯影，转场到法国埃菲尔铁塔下。第一人称穿过巴黎广场，抬头看见铁塔直入蓝天，周围游客、喷泉和街道建筑形成浪漫城市氛围。 *[gloss: The view moves on; the lake's reflections become city lights and the scene transitions to the foot of the Eiffel Tower. The first-person view crosses a Paris square, looking up at the tower against blue sky, with tourists, fountains, and street architecture forming a romantic city atmosphere.]*
- `4` **Key 4** — 夕阳光芒扩散，来到日本富士山脚下。第一人称沿着樱花小路前进，粉色花瓣随风飘落，远处富士山覆盖白雪，湖面倒映着山影和天空。 *[gloss: Sunset light spreads and the view arrives at the foot of Mount Fuji. The first-person view follows a cherry-blossom path, pink petals drifting down, snow-capped Fuji in the distance, the lake reflecting mountain and sky.]*
- `5` **Key 5** — 镜头穿过一道光影，来到印度泰姬陵前。第一人称沿着水池中轴线向前移动，白色大理石宫殿倒映在水面上，花园、拱门和远处飞鸟让场景显得宁静庄严。 *[gloss: The camera passes through a band of light and arrives before the Taj Mahal. The first-person view moves along the reflecting pool's axis, the white marble palace mirrored in the water, gardens, archways, and distant birds lending the scene calm grandeur.]*
- `6` **Key 6** — 画面被水雾吞没，转化到巴西基督像所在的山顶。第一人称沿观景平台行走，脚下是里约城市与海湾，巨大的基督像展开双臂，云层从身边缓缓飘过。 *[gloss: The frame is swallowed by water mist and transforms to the hilltop of Christ the Redeemer in Brazil. The first-person view walks the viewing platform, Rio's city and bay below, the giant statue spreading its arms, clouds drifting slowly past.]*
- `7` **Key 7** — 最后画面来到美国旧金山金门大桥。第一人称沿着桥面人行道向前移动，橙红色桥塔高耸在海雾之中，钢索向远处延伸，脚下是海湾与来往船只，远处城市天际线若隐若现，旅程在壮阔的桥梁景观中结束。 *[gloss: Finally the view arrives at the Golden Gate Bridge in San Francisco. The first-person view moves along the walkway, the orange-red towers rising through sea fog, cables stretching into the distance, the bay and passing ships below, the city skyline half-visible — the journey ends in the sweeping bridge vista.]*
- `space` **Jump** — The character jumps high into the air.
