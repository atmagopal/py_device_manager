#!/usr/bin/python3

import os

class AudioDeviceManager():

    def __init__(self):
        self.sinks      = self.Sinks()
        self.sources    = self.Sources()

    def resetAudio(self):
        """ Reset the audio manager daemon
        """
        os.popen('pulseaudio -k')

    class Sinks():
        def getSinkStreamIndices(self):
            """ Get indices of active output audio streams, i.e. processes that have audio output.

            Returns:
                (list, list): indices of active audio streams, according sink names
            """
            streams = os.popen('pacmd list-sink-inputs| grep index:').readlines()
            sinks   = os.popen('pacmd list-sink-inputs| grep sink:').readlines()
            
            active_streams = []
            active_sinks   = []

            for i in range(len(streams)):
                stream = streams[i]
                index = int(stream.split(': ')[1].split('\n')[0])
                active_streams.append(index)
                
                sink = sinks[1]
                name = sink.split('<')[1].split('>')[0]
                active_sinks.append(name)

            return active_streams, active_sinks


        def getCurrentSinkDevice(self):
            """ Get current sink

            Returns:
                tuple: (str) description, (str) device name, (int) device_index 
            """
            device = os.popen('pactl info | grep Sink:').readlines()
            name   = device[0].split(': ')[1].split('\n')[0]

            allSinks = self.getAvailableSinks()
            for sink in allSinks:
                sink_value = allSinks[sink] 
                if name in sink_value:
                    return sink_value 

            raise BaseException("Default sink not found in list of sinks.")


        def getAvailableSinks(self):
            """ Get index and name of audio outputs in the system.

            Returns:
                dict: Dict of audio sinks detected -> key: (int) index; item: (str) description, (str) device name, (int) device_index 
            
            Raises:
                BaseException: When no audio devices found
            """
            sinks = os.popen('pactl list short sinks').readlines()
            descriptions = os.popen('pactl list sinks |grep Description: ').readlines()
        
            if len(sinks) == 0:
                print("No audio devices detected. Check if 'pactl' commands work on your terminal.")
                raise BaseException('No audio devices detected. Check if pactl commands work on your terminal.')

            sinks_dict = dict()

            for x in range(len(sinks)):
                sink        = sinks[x]
                index       = int(sink.split('\t')[0])
                device      = sink.split('\t')[1]
                description = descriptions[x].split(': ')[1].split('\n')[0]
                sinks_dict[x] = description, device, index
            
            return sinks_dict

        def getSinkDescriptions(self):
            """ Get understandable device description

            Returns:
                list(str): Device descr.
            """
            allSinks = self.getAvailableSinks()
            descriptions = []
            for sink in allSinks:
                descriptions.append(allSinks[sink][0])
            
            return descriptions
            

        def switchSinkDevice(self, deviceDescription):
            """ Switch audio sink device

            Args:
                deviceDescription (int): chosen audio device descr.

            Raises:
                BaseException: Audio device switch failure.
            """
            allSinks = self.getAvailableSinks()
            for sink in allSinks:
                # Is chosen sink?
                if deviceDescription in allSinks[sink]:
                    deviceIndex = allSinks[sink][2]
                    resp = os.popen('pacmd set-default-sink {}'.format(deviceIndex)).readlines()
            
                    streamIndices = self.getSinkStreamIndices()[0]
                    for stream in streamIndices:
                        resp.append(os.popen('pacmd move-sink-input {} {}'.format(stream, deviceIndex)).readlines())
            
                    for x in resp:
                        if 'Error' in x or 'Failed' in x:
                            print(x)
                            raise BaseException(x)
                    
                    # Check if current default sink == new choice
                    if self.getCurrentSinkDevice()[2] == deviceIndex:
                        stream_sinks = self.getSinkStreamIndices()[1]
                        current_sink_name = self.getCurrentSinkDevice()[1]
                        
                        # Check if all streams switched successfully 
                        for sink in stream_sinks:
                            if current_sink_name not in sink: 
                                raise BaseException('Not all streams were switched. Please try again.')

                        print('Audio sink device switch successful')
                        return
                    else:
                        raise BaseException('Audio sink device switch failed')

            raise BaseException('Audio sink device switch failed')

    class Sources():
        def getSourceStreamIndices(self):
            """ Get indices of active input audio streams, i.e. processes that have audio output.

            Returns:
                list: indices of active audio streams
            """
            streams = os.popen('pacmd list-source-outputs| grep index:').readlines()
            sources = os.popen('pacmd list-source-outputs| grep source:').readlines()
            
            active_streams = []
            active_sources = []

            for i in range(len(streams)):
                stream = streams[i]
                index = int(stream.split(': ')[1].split('\n')[0])
                active_streams.append(index)

                source = sources[i]
                name = source.split('<')[1].split('>')[0]
                active_sources.append(name)

            return active_streams, active_sources
        

        def getCurrentSourceDevice(self):
            """ Get current source

            Returns:
                tuple: (str) description, (str) device name, (int) device_index 
            """
            device = os.popen('pactl info | grep Source:').readlines()
            name   = device[0].split(': ')[1].split('\n')[0]

            allSources = self.getAvailableSources()
            for source in allSources:
                source_value = allSources[source] 
                if name in source_value:
                    return source_value

            raise BaseException("Default source not found in list of sources.")


        def getAvailableSources(self):
            """ Get index and name of audio outputs in the system.

            Returns:
                dict: Dict of audio sources detected -> key: (int) index; item: (str) description, (str) device name, (int) device_index
            
            Raises:
                BaseException: When no input audio devices found
            """
            sources = os.popen('pactl list short sources').readlines()
            descriptions = os.popen('pactl list sources |grep Description: ').readlines()
        
            if len(sources) == 0:
                print("No audio input devices detected. Check if 'pactl' commands work on your terminal.")
                raise BaseException('No audio input devices detected. Check if pactl commands work on your terminal.')

            sources_dict = dict()
            i = 0 # Key for dict

            for x in range(len(sources)):
                source = sources[x]
                if 'input' in source or 'source' in source:
                    index       = int(source.split('\t')[0])
                    device      = source.split('\t')[1]
                    description = descriptions[x].split(': ')[1].split('\n')[0]
                    sources_dict[i] = description, device, index
                    i += 1 # increment only if valid
            
            return sources_dict
        
        def getSourceDescriptions(self):
            """ Get understandable device description

            Returns:
                list(str): Device descr.
            """
            allSources = self.getAvailableSources()
            descriptions = []
            for source in allSources:
                descriptions.append(allSources[source][0])
            
            return descriptions
        
        def switchSourceDevice(self, deviceDescription):
            """ Switch audio source device

            Args:
                deviceDescription (int): audio device descr.

            Raises:
                BaseException: Audio device switch failure.
            """
            allSources = self.getAvailableSources()
            for source in allSources:
                # Is chosen source?
                if deviceDescription in allSources[source]:
                    deviceIndex = allSources[source][2]
                    resp = os.popen('pacmd set-default-source {}'.format(deviceIndex)).readlines()

                    streamIndices =  self.getSourceStreamIndices()[0]
                    for stream in streamIndices:
                        resp.append(os.popen('pacmd move-source-output {} {}'.format(stream, deviceIndex)).readlines())

                    for x in resp:
                        if 'Error' in x or 'Failed' in x:
                            print(x)
                            raise BaseException(x)
                    
                    # Check if current default source == new choice
                    if self.getCurrentSourceDevice()[2] == deviceIndex:
                        stream_sources = self.getSourceStreamIndices()[1]
                        current_source_name = self.getCurrentSourceDevice()[1]

                        # Check if all streams switched successfully 
                        for sink in stream_sources:
                            if current_source_name not in sink: 
                                raise BaseException('Not all streams were switched. Please try again.')

                        print('Audio source device switch successful')
                        return
                    else:
                        raise BaseException('Audio source device switch failed')

            raise BaseException('Audio source device switch failed')

