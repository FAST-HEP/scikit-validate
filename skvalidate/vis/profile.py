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
    fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot(111)
    this, = ax.plot(profile['timestamp'], profile['mem_usage'], label='this code')
    ref, = ax.plot(profile_ref['timestamp'], profile_ref['mem_usage'], label='reference')
    plt.title(title)
    plt.xlabel('time [s]')
    plt.ylabel('RSS [MB]')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), ncol=2)

    max_y = max(profile['mem_usage'] + profile_ref['mem_usage']) * 1.1
    plt.ylim((0, max_y))
    fig.tight_layout()
    fig.savefig(output)
