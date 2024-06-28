"""
General config module
"""
from pathlib import Path
from typing import Union

import spikeinterface.extractors as se


RDS_RAW_PATH = Path('/mnt/rds/me24/projects/beneuro/live/raw')
RDS_PROC_PATH = Path('/mnt/rds/me24/projects/beneuro/live/processed')


class expConfig:

    def __init__(self, animal: str, probes: tuple = ('imec0', 'imec1')) -> None:
        # Animal
        self.animal = animal

        # Sessions
        self.raw_sessions = self.get_all_sessions(RDS_RAW_PATH)
        self.raw_ephys_sessions = self.get_ephys_sessions(self.raw_sessions)

        # Probes
        self.probes = probes
        

    def get_all_sessions(self, base_path: Path):

        directory = base_path / self.animal
        sessions = [f for f in directory.iterdir() if f.is_dir()]
        return sessions
    
    def get_ephys_sessions(self, sessions: Path):
        ephys_sessions = []
        for sess in sessions:            
            ephys_folders = list(sess.glob('*_g0'))
            if ephys_folders:
                ephys_sessions.append(ephys_folders[0])
        if ephys_sessions:
            print(f'Found raw ephys sessions')
        
        return ephys_sessions
    
    def get_raw_recordings(self):
        recordings = {}
        for idx, ephys_session in enumerate(self.raw_ephys_sessions):
            recordings[f'ses-{idx+1}'] = {}
            print(f'Accessing session {idx+1} (ses-{idx+1}) {ephys_session.name}...')
            for probe in self.probes:
                recording_lf = se.read_spikeglx(
                    ephys_session,
                    stream_name=f'{probe}.lf'
                )
                print(f'\tProbe {probe} LFP recording:\n\t\t'
                      f'Num. channels: {recording_lf.get_num_channels()}'
                      f'\n\t\tDuration: {round(recording_lf.get_duration())} seconds',
                      f'\n\t\tSampling freq: {round(recording_lf.get_sampling_frequency())} Hz')

                recording_ap = se.read_spikeglx(
                    ephys_session,
                    stream_name=f'{probe}.ap'
                )
                print(f'\tProbe {probe} AP recording:\n\t\t'
                      f'Num. channels: {recording_ap.get_num_channels()}'
                      f'\n\t\tDuration: {round(recording_ap.get_duration())} seconds',
                      f'\n\t\tSampling freq: {round(recording_ap.get_sampling_frequency())} Hz')
                recordings[f'ses-{idx+1}'][f'{probe}'] = (recording_lf, recording_ap)
        return recordings




