import Augmentor
p = Augmentor.Pipeline("./Apps/database/circles_samples")
#  no cropping, be careful of zoom feature
p.rotate_without_crop(probability=1, max_left_rotation=180, max_right_rotation=180)
p.flip_left_right(probability=0.5)
p.flip_top_bottom(probability=0.5)
p.zoom_random(probability=0.3, percentage_area=0.8)  # test once running on real images
p.sample(50)
