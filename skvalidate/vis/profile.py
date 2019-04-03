from plumbum import local
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['lines.linewidth'] = 4
matplotlib.rcParams['axes.titlesize'] = 40
matplotlib.rcParams['axes.labelsize'] = 32
matplotlib.rcParams['xtick.labelsize'] = 32
matplotlib.rcParams['ytick.labelsize'] = 32
matplotlib.rcParams['legend.fontsize'] = 32

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
    fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot(111)
    this, = ax.plot(profile['timestamp'], profile['mem_usage'], label='this code')
    ref, = ax.plot(profile_ref['timestamp'], profile_ref['mem_usage'], label='reference')
    plt.title(title, fontsize=40)
    plt.xlabel('time [s]', fontsize=40)
    plt.ylabel('RSS [MB]', fontsize=40)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), ncol=2)

    max_y = max(profile['mem_usage'] + profile_ref['mem_usage']) * 1.1
    plt.ylim((0, max_y))
    fig.tight_layout()
    fig.savefig(output)
