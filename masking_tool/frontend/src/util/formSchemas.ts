import { RJSFSchema, UiSchema } from "@rjsf/utils";

export const blurFormSchemaSubjectBBox: RJSFSchema = {
  type: 'object',
  properties: {
    subjectDetection: {
      type: 'string',
      title: 'Subject Detection (Localization) Method',
      enum: ['yolo'],
      default: 'yolo',
      description: 'The model that should be used for subject detection (localization).'
    },
    hidingParams: {
      type: "object",
      properties: {
        kernelSize: { type: 'integer', title: 'Kernel Size', default: 23, description: 'The Kernelsize for a Gaussion Filter' },
        extraPixels: { type: 'number', title: "Additional pixels", default: 0, description: "Additional pixels to lay around the detected subject to ensure even further that it is masked completely." }
      }
    }
  },
  dependencies: {
    subjectDetection: {
      oneOf: [
        {
          properties: {
            subjectDetection: { enum: ['yolo'] },
            detectionParams: {
              type: "object",
              properties: {
                numPoses: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of subjects which can be detected' },
                confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the detection to be considered successful.' },
              }
            },
          },
        }
      ]
    },
  },
};

export const blurFormSchemaSubjectSilhouette: RJSFSchema = {
  type: 'object',
  properties: {
    subjectDetection: {
      type: 'string',
      title: 'Subject Detection (Localization) Method',
      enum: ['yolo', 'mediapipe'],
      default: 'mediapipe',
      description: 'The model that should be used for subject detection (localization).'
    },
    hidingParams: {
      type: "object",
      properties: {
        kernelSize: { type: 'integer', title: 'Kernel Size', default: 23, description: 'The Kernelsize for a Gaussion Filter' },
        extraPixels: { type: 'number', title: "Additional pixels", default: 0, description: "Additional pixels to lay around the detected subject to ensure even further that it is masked completely." }
      }
    }
  },
  dependencies: {
    subjectDetection: {
      oneOf: [
        {
          properties: {
            subjectDetection: { enum: ['yolo'] },
            detectionParams: {
              type: "object",
              properties: {
                numPoses: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of subjects which can be detected' },
                confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the detection to be considered successful.' },
              }
            },
          },
        },
        {
          properties: {
            subjectDetection: { enum: ['mediapipe'] },
            detectionParams: {
              type: "object",
              properties: {
                numPoses: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of subjects which can be detected' },
                confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the detection to be considered successful.' },
              }
            },
          },
        }
      ]
    },
  },
};

export const blurFormSchemaSubjectUI: UiSchema = {
  'ui:order': ['subjectDetection', 'detectionModel', 'detectionParams', 'hidingParams'],
};

export const blackoutFormSchemaSubjectBBox: RJSFSchema = {
  type: 'object',
  properties: {
    subjectDetection: {
      type: 'string',
      title: 'Subject Detection (Localization) Method',
      enum: ['yolo'],
      default: 'yolo',
      description: 'The model that should be used for subject detection (localization).'
    },
    hidingParams: {
      type: "object",
      properties: {
        color: { type: 'number', title: 'Masking color', default: 0, description: 'From 0 (black) to 255 white' },
        extraPixels: { type: 'number', title: "Additional pixels", default: 0, description: "Additional pixels to lay around the detected subject to ensure even further that it is masked completely." }
      }
    }
  },
  dependencies: {
    subjectDetection: {
      oneOf: [
        {
          properties: {
            subjectDetection: { enum: ['yolo'] },
            detectionParams: {
              type: "object",
              properties: {
                numPoses: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of subjects which can be detected' },
                confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the detection to be considered successful.' },
              }
            },
          },
        }
      ]
    },
  },
};

export const blackoutFormSchemaSubjectSilhouette: RJSFSchema = {
  type: 'object',
  properties: {
    subjectDetection: {
      type: 'string',
      title: 'Subject Detection (Localization) Method',
      enum: ['yolo', 'mediapipe'],
      default: 'mediapipe',
      description: 'The model that should be used for subject detection (localization).'
    },
    hidingParams: {
      type: "object",
      properties: {
        color: { type: 'number', title: 'Masking color', default: 0, description: 'From 0 (black) to 255 white' },
        extraPixels: { type: 'number', title: "Additional pixels", default: 0, description: "Additional pixels to lay around the detected subject to ensure even further that it is masked completely." }
      }
    }
  },
  dependencies: {
    subjectDetection: {
      oneOf: [
        {
          properties: {
            subjectDetection: { enum: ['yolo'] },
            detectionParams: {
              type: "object",
              properties: {
                numPoses: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of subjects which can be detected' },
                confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the detection to be considered successful.' },
              }
            },
          },
        },
        {
          properties: {
            subjectDetection: { enum: ['mediapipe'] },
            detectionParams: {
              type: "object",
              properties: {
                numPoses: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of subjects which can be detected' },
                confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the detection to be considered successful.' },
              }
            },
          },
        }
      ]
    },
  },
};

export const blackoutFormSchemaSubjectUI: UiSchema = {
  'ui:order': ['detectionParams', 'hidingParams'],
};

export const blurFormSchemaBG: RJSFSchema = {
  type: 'object',
  properties: {
    kernelSize: { type: 'integer', title: 'Kernel Size', default: 23, description: 'The Kernelsize for a Gaussion Filter' },
  },
};

export const blackoutFormSchemaBG: RJSFSchema = {
  type: 'object',
  properties: {
    color: { type: 'number', title: 'Masking color', default: 0, description: 'From 0 (black) to 255 white' },
  },
};

export const skeletonFormSchema: RJSFSchema = {
  type: 'object',
  properties: {
    maskingModel: { title: 'The model that should be used for creating a skeleton.', type: 'string', default: 'mediapipe', enum: ['mediapipe'] },
    numPoses: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of subjects which can be detected' },
    confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the detection to be considered successful.' },
    timeseries: { type: 'boolean', title: 'Save output as timeseries in CSV', default: false },
  },
}

export const faceMeshFormSchema: RJSFSchema = {
  type: 'object',
  properties: {
    maskingModel: { title: 'The model that should be used for creating a face mesh.', type: 'string', default: 'mediapipe', enum: ['mediapipe'] },
    numFaces: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of faces which can be detected' },
    confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the face detection to be considered successful.' },
    timeseries: { type: 'boolean', title: 'Save output as timeseries in CSV', default: false },
  },
};

export const skeletonFaceMeshFormSchema: RJSFSchema = {
  type: 'object',
  properties: {
    maskingModel: { title: 'The model that should be used for creating a face mesh.', type: 'string', default: 'mediapipe', enum: ['mediapipe'] },
    numPoses: { type: 'number', title: 'Num Subjects', default: 1, description: 'The maximum number of faces which can be detected' },
    confidence: { type: 'number', title: 'Confidence', default: 0.5, description: 'The minimum confidence score for the face detection to be considered successful.' },
    timeseries: { type: 'boolean', title: 'Save output as timeseries in CSV', default: false },
  },
};

export const bodyMeshFormSchema: RJSFSchema = {
  type: 'object',
  properties: {
    maskingModel: { title: 'The model that should be used for the body mesh.', type: 'string', default: 'vibe', enum: ['vibe'] },
    timeseries: { type: 'boolean', title: 'Save output as timeseries in CSV', default: false },
  },
};