# Goals
- Must provide a way to create ambiences
- Must provide a way to edit ambiences
- Must be able to play ambiences
- Must be able to play multiple ambiences at once
- Must be able to transition between ambiences

# Documentation
## Ambience files
Each ambience is saved as a json file, containing all the information about the
individual tracks and their properties in the context of the ambience.

Example structure:
```json
{
  "options": {
      "volume": 100
  },
  "sounds": {
    "sound1": {
      "source_type": "local, remote, spotify, ...",
      "source": "/path/to/file.mp3",
      "pause_ms": 0,
      "overlap_ms": 100,
      "meander": true
    },
    "sound2": {
      "source_type": "local, remote, spotify, ...",
      "source": "/path/to/file.mp3, https://path.com/to/remote.mp3",
      "volume": 100,
      "pause_ms": 0,
      "overlap_ms": 100,
      "meander": true
    }
  }
}
```
