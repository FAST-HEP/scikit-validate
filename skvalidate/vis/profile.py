from plumbum import local
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

def plot_memory_profile(input_files, output_file, title=None):
    mprof = local['mprof']
    params = ['plot']
    params += input_files
    params += []
    params = [
        'plot',
        ' '.join(input_files),
        '--output={}'.format(output_file),
    ]
    if title:
        params.append('--title {}'.format(title))

    mprof[params]

def draw_profiles(profiles, profiles_ref, outputs):
    for command, profile in profiles.items():
        profile_ref = profiles_ref[command]

        draw_profile(
            profile, profile_ref,
            title=command,
            output=outputs[command],
        )

def draw_profile(profile, profile_ref, title, output, **kwargs):
    pass
