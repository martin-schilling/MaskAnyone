import { Button, Dialog, DialogTitle, DialogContent, DialogContentText, TextField, DialogActions, IconButton } from "@mui/material"
import { Fragment, createRef, useState } from "react"
import TuneIcon from '@mui/icons-material/Tune';
import validator from '@rjsf/validator-ajv8';
import Form from '@rjsf/mui';
import { RJSFSchema, UiSchema } from "@rjsf/utils";
import { IChangeEvent } from "@rjsf/core";

interface MethodSettingProps {
    children?: React.ReactNode
    formSchema?: RJSFSchema,
    uiSchema?: UiSchema,
    methodName?: string,
    values?: { [paramterName: string]: any }
    onSet: (params: object) => void
}

const MethodSettings = (props: MethodSettingProps) => {
    const [open, setOpen] = useState(false)
    const { formSchema, uiSchema, methodName, values, onSet } = props

    const submitFormRef: React.RefObject<HTMLInputElement> = createRef();

    const onSetOpen = () => {
        // @todo reset params to global form
        setOpen(true)
    }

    const onSubmit = ({ formData }: IChangeEvent<any, RJSFSchema, any>, e: React.FormEvent<any>) => {
        onSet(formData)
    }

    const handleParamsSet = () => {
        if (submitFormRef.current) {
            submitFormRef.current.click()
            setOpen(false)
        } else {
            throw "submitFormRef not set"
        }
    }

    if (!methodName || !formSchema) {
        return (
            <div>
                <IconButton aria-label="Adjust method parameters" disabled={true}>
                    <TuneIcon />
                </IconButton>
            </div>
        )
    }

    return (
        <div>
            <IconButton onClick={onSetOpen} aria-label="Adjust method parameters">
                <TuneIcon />
            </IconButton>

            <Dialog open={open} onClose={() => setOpen(false)}>
                <DialogTitle>Customize parameters for {methodName}</DialogTitle>
                <DialogContent>
                    <Form
                        schema={formSchema}
                        validator={validator}
                        onSubmit={onSubmit}
                        formData={values}
                        uiSchema={uiSchema}
                    >
                        <input ref={submitFormRef} type="submit" style={{ display: "none" }} />
                    </Form>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpen(false)}>Cancel</Button>
                    <Button onClick={() => handleParamsSet()}>Set</Button>
                </DialogActions>
            </Dialog>
        </div>
    )
}

export default MethodSettings