"""
General config module
"""
import os
import glob
from pathlib import Path


RDS_RAW_PATH = Path('/mnt/rds/me24/projects/beneuro/live/raw')
RDS_PROC_PATH = Path('/mnt/rds/me24/projects/beneuro/live/processed')


class expConfig:


    def __init__(self, animal: str, session: int) -> None:
        self.animal = animal

        # Sessions
        self.raw_sessions = self.get_all_sessions(RDS_RAW_PATH)
        self.raw_ephys_sessions = self.get_ephys_sessions(self.raw_sessions)
        self.proc_sessions = self.get_all_sessions(RDS_PROC_PATH)
        self.session = session


    def get_all_sessions(self, base_path):

        directory = base_path / self.animal
        sessions = [f for f in directory.iterdir() if f.is_dir()]
        return sessions
    
    def get_ephys_sessions(self, sessions: Path):
        ephys_sessions = []
        for sess in sessions:            
            pattern='*_g0'
            matching_subfolders = [f for f in sess.glob(pattern) if f.is_dir()]
            if matching_subfolders:
                ephys_sessions.append(sess)
                print(f'Found session with raw ephys data: {sess.name}')
        return ephys_sessions

