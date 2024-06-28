"""
General config module
"""
from pathlib import Path
from typing import Union


RDS_RAW_PATH = Path('/mnt/rds/me24/projects/beneuro/live/raw')
RDS_PROC_PATH = Path('/mnt/rds/me24/projects/beneuro/live/processed')


class expConfig:

    def __init__(self, animal: str, session_idx: Union[None, int] = None) -> None:
        # Animal
        self.animal = animal

        # Sessions
        self.raw_sessions = self.get_all_sessions(RDS_RAW_PATH)
        self.raw_ephys_sessions = self.get_ephys_sessions(self.raw_sessions)
        self.session_idx = session_idx
        self.session = self.raw_ephys_sessions[self.session_idx]
        


    def get_all_sessions(self, base_path):

        directory = base_path / self.animal
        sessions = [f for f in directory.iterdir() if f.is_dir()]
        return sessions
    
    def get_ephys_sessions(self, sessions: Path):
        ephys_sessions = []
        for sess in sessions:            
            ephys_folders = list(sess.glob('*_g0'))
            if ephys_folders:
                print(f'Found raw ephys session: {ephys_folders[0].name}')
                ephys_sessions.append(ephys_folders[0])
        
        return ephys_sessions

