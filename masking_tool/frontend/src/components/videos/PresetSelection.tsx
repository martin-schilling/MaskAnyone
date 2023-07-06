import { Button, Grid, Paper, Typography } from "@mui/material";
import { Box } from "@mui/system";
import PresetItem from "./PresetItem";
import TuneIcon from '@mui/icons-material/Tune';
import { useState } from "react";
import { Preset, RunParams } from "../../state/types/Run";
import { maskingMethods } from "../../util/maskingMethods";

interface PresetSelectionProps {
    onPresetSelect: (preset: Preset) => void
    onCustomModeRequested: () => void
    selectedPreset?: Preset
}

const mockPresets: Preset[] = [
    {
        name: "Blur Face",
        detailText: "This preset will blur the face of detected persons in the video. Only the face will be blurred, the rest of the video will stay untouched.",
        runParams: {
            videoMasking: {
                "body": {
                    hidingStrategy: {
                        key: "none",
                        params: {}
                    }, maskingStrategy: {
                        key: "none",
                        params: {}
                    }
                },
                "head": {
                    hidingStrategy: {
                        key: "blur",
                        params: maskingMethods["body"].hidingMethods!["blur"].defaultValues!
                    }, maskingStrategy: {
                        key: "none",
                        params: {}
                    }
                },
                "background": {
                    hidingStrategy: {
                        key: "none",
                        params: {}
                    }, maskingStrategy: {
                        key: "none",
                        params: {}
                    }
                }
            },
            threeDModelCreation: {
                skeleton: false,
                skeletonParams: {},
                blender: false,
                blenderParams: {},
                blendshapes: false,
                blendshapesParams: {}
            },
            voiceMasking: {}
        }
    },
    {
        name: "Mask Kinematics",
        runParams: {
            videoMasking: {
                "body": {
                    hidingStrategy: {
                        key: "blackout",
                        params: maskingMethods["body"].hidingMethods["blackout"].defaultValues!
                    }, maskingStrategy: {
                        key: "skeleton",
                        params: maskingMethods["body"].maskingMethods!["skeleton"].defaultValues!
                    }
                },
                "head": {
                    hidingStrategy: {
                        key: "blackout",
                        params: maskingMethods["head"].hidingMethods["blackout"].defaultValues!
                    }, maskingStrategy: {
                        key: "skeleton",
                        params: maskingMethods["head"].maskingMethods!["skeleton"].defaultValues!
                    }
                },
                "background": {
                    hidingStrategy: {
                        key: "none",
                        params: {}
                    }, maskingStrategy: {
                        key: "none",
                        params: maskingMethods["background"].hidingMethods!["blur"].defaultValues!
                    }
                }
            },
            threeDModelCreation: {
                skeleton: false,
                skeletonParams: {},
                blender: false,
                blenderParams: {},
                blendshapes: false,
                blendshapesParams: {}
            },
            voiceMasking: {}
        }
    },
    {
        name: "Video to 3D Character",
        runParams: {
            videoMasking: {},
            threeDModelCreation: {
                skeleton: false,
                skeletonParams: {},
                blender: false,
                blenderParams: {},
                blendshapes: false,
                blendshapesParams: {}
            },
            voiceMasking: {}
        }
    },
    {
        name: "Replace Face (Coming Soon!)",
        runParams: {
            videoMasking: {},
            threeDModelCreation: {
                skeleton: false,
                skeletonParams: {},
                blender: false,
                blenderParams: {},
                blendshapes: false,
                blendshapesParams: {}
            },
            voiceMasking: {}
        }
    },
    {
        name: "Blur Background",
        runParams: {
            videoMasking: {
                "body": {
                    hidingStrategy: {
                        key: "none",
                        params: {}
                    }, maskingStrategy: {
                        key: "none",
                        params: {}
                    }
                },
                "head": {
                    hidingStrategy: {
                        key: "none",
                        params: {}
                    }, maskingStrategy: {
                        key: "none",
                        params: {}
                    }
                },
                "background": {
                    hidingStrategy: {
                        key: "blur",
                        params: {}
                    }, maskingStrategy: {
                        key: "none",
                        params: {}
                    }
                }
            },
            threeDModelCreation: {
                skeleton: false,
                skeletonParams: {},
                blender: false,
                blenderParams: {},
                blendshapes: false,
                blendshapesParams: {}
            },
            voiceMasking: {}
        }
    },
]

const PresetSelection = (props: PresetSelectionProps) => {
    const [presets, setPresets] = useState(mockPresets)
    const { selectedPreset } = props

    const onPresetClicked = (preset: Preset) => {
        props.onPresetSelect(preset)
    }

    return (
        <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }} xs={12} marginTop={"10px"}>
            {presets.map((preset, index) => (
                <Grid item xs={4} key={preset.name}>
                    <PresetItem
                        name={preset.name}
                        selected={selectedPreset ? selectedPreset.name == preset.name : false}
                        previewImagePath={preset.previewImagePath}
                        description={preset.detailText}
                        onClick={() => onPresetClicked(preset)}
                    />
                </Grid>
            ))}
            <Grid item xs={4}>
                <PresetItem
                    name="Custom Run"
                    icon={<TuneIcon />}
                    selected={false}
                    onClick={() => props.onCustomModeRequested()}
                />
            </Grid>
        </Grid>
    )
}

export default PresetSelection