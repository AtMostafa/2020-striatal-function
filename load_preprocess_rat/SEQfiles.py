import sys, struct, logging
import io, time
from datetime import timedelta
from PIL import Image

class SeqFileFormat:
    HEADER={
        'numOfFrames':  {'offset':572, 'L':4, 'format':'=L'},
        'headerSize':   {'offset': 32, 'L':4, 'format':'=l'},
        'fixedSize':    {'offset':600, 'L':4, 'format':'=L'},
        'timeOffset':   {'offset':612, 'L':4, 'format':'=l'},
        'compression':  {'offset':620, 'L':4, 'format':'=l'},
    }
    
    TIMESTAMP={
        'offset':0,
        'L':8,
        'format':'=lHH'
    }
    def __init_subclass__(cls,*args):
        assert hasattr(cls, '__enter__'), f"{cls.__name__} is not a context manager!"
        
    def _read_frame_size(self):
        fameSizeByte=self.file.read(4)
        
        return int.from_bytes(fameSizeByte,sys.byteorder)-4
    
    def _read_timestamp(self):
        timestampByte=self.file.read(self.TIMESTAMP['L'])
        timestamp=struct.unpack(self.TIMESTAMP['format'],timestampByte)
        
        time=timedelta(seconds=timestamp[0], milliseconds=timestamp[1], microseconds=timestamp[2])
        
        return time

class SeqFile(SeqFileFormat):
    """
    This class implements basic methods to extract single frames from a 
    norpix *.SEQ movie file WITH jpeg compression.
    Interface:
    with SeqFile(path_to_file) as f:
        f.goto_time (time_to_go_to_as_a_deltatime_object) OR f.goto_frame(frame_number)
        frameImage, timeStamp = f.get_frame()
    """

    def __init__(self, filePath):
        self.filePath=filePath

    @classmethod
    def open(cls, *arg, **kw):
        obj=cls(*arg, **kw)
        return obj.__enter__()
        
    def _peek(self, size, offset, from_what=0):
        """
        read a few bytes from an offset without moving the file pointer
        """
        f_init=self.file.tell()
        try:
            self.file.seek(offset, from_what)
            data=self.file.read(size)
        finally:
            self.file.seek(f_init)
            
        return data
        
    def __enter__(self):
        try:
            self.file = open(self.filePath,'rb')
        except Exception as e:
            logging.error(f"file: {self.arg} failed to open!\n{repr(e)}")
            return None
        
        return self

    def __exit__(self, *args):
        try:
            self.file.close()
        except AttributeError:
            #when there is an error in opening the file, so there is no close() method
            pass
    
    def num_of_frames(self):
        data= self._peek(self.HEADER['numOfFrames']['L'],self.HEADER['numOfFrames']['offset'])
        return struct.unpack(self.HEADER['numOfFrames']['format'],data)[0]
    
    def time_offset(self):
        """
        this method returns the timestamp of the first frame
        """
        headerByte=self._peek(self.HEADER['headerSize']['L'],self.HEADER['headerSize']['offset'])
        headerSize=struct.unpack(self.HEADER['headerSize']['format'],headerByte)[0]

        frame1sizeByte=self._peek(4,headerSize)
        frame1size=int.from_bytes(frame1sizeByte,sys.byteorder)-4

        timeByte=self._peek(self.TIMESTAMP['L'],headerSize+4+frame1size)
        timestamp=struct.unpack(self.TIMESTAMP['format'],timeByte)
        
        time=timedelta(seconds=timestamp[0], milliseconds=timestamp[1], microseconds=timestamp[2])
        return time

    def get_frame(self):
        """
        this method yields one frame image.
        the pointer must be at the begining of a frame (frame size byte)
        reaching the end will raise an error
        """
        frameSize=self._read_frame_size()
        imageByte=self.file.read(frameSize)
        
        image = Image.open(io.BytesIO(imageByte))
        timestamp=self._read_timestamp()
        return image, timestamp

    def goto_frame(self,N=1):
        """
        This method browses the pointer to the begining of the N_th frame
        """
        headerByte=self._peek(self.HEADER['headerSize']['L'],self.HEADER['headerSize']['offset'])
        headerSize=struct.unpack(self.HEADER['headerSize']['format'],headerByte)[0]
        #pre-allocation to incease the speed
        timestampL=self.TIMESTAMP['L']
        byteorder= sys.byteorder
        file=self.file
        
        file.seek(headerSize)
        n=1
        while n<=N:
            fameSizeByte=file.read(4)
            frameSize= int.from_bytes(fameSizeByte,byteorder)-4
            file.seek(frameSize+timestampL,1)
            n+=1
        logging.info(f'current frame:{n}')
            
    def goto_time(self,T=0):
        """
        this method browses the file to the begining of a frame, closest to the time T
        """
        if T==0:
            T=self.time_offset()
        
        assert isinstance(T,timedelta), 'Bad time format'
        
        if T.days <= 1: #in case T is not relative to first frame
            T=T-self.time_offset()
            
        headerByte=self._peek(self.HEADER['headerSize']['L'],self.HEADER['headerSize']['offset'])
        headerSize=struct.unpack(self.HEADER['headerSize']['format'],headerByte)[0]
        #pre-allocation to incease the speed
        timestampL     =self.TIMESTAMP['L']
        timestampFormat=self.TIMESTAMP['format']
        byteorder= sys.byteorder
        file=self.file
        
        file.seek(headerSize)
        dt=timedelta(days=2)
        zero=timedelta()
        while dt>=zero:
            fameSizeByte=file.read(4)
            frameSize= int.from_bytes(fameSizeByte,byteorder)-4
            file.seek(frameSize,1)
            timeByte=file.read(timestampL)
            timestamp=struct.unpack(timestampFormat,timeByte)
            time=timedelta(seconds=timestamp[0], milliseconds=timestamp[1], microseconds=timestamp[2])
            dt=T-time
        
        file.seek(-(frameSize+timestampL+4),1)
        logging.info(f'current time:{time}')
        
if __name__=="__main__":
    filePath="/data/Rat106/Experiments/Rat106_2017_03_31_10_56/Rat106_2017_03_31_10_56.seq"
    t0=time.perf_counter()
    with SeqFile(filePath) as f:
        t=f.time_offset()
        T=t+timedelta(minutes=44)
        f.goto_time(T)
        im,_=f.get_frame()
        im.show()
        t1=time.perf_counter()
        print(f'Done:{t1-t0}')

