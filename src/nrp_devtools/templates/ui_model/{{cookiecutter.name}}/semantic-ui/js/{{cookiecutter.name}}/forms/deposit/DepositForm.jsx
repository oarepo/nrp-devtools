{% raw -%}
import React from "react";
import _isEmpty from "lodash/isEmpty";
import { BaseForm, TextField, FieldLabel } from "react-invenio-forms";
import { Container, Grid, Ref, Sticky, Card } from "semantic-ui-react";
import { DepositValidationSchema } from "./DepositValidationSchema";
import {
  useFormConfig,
  FormFeedback,
  FormikStateLogger,
  SaveButton,
  PreviewButton,
  PublishButton,
  ValidateButton,
  DeleteButton,
} from "@js/oarepo_ui";
import Overridable from "react-overridable";

export const DepositForm = () => {
  const { record } = useFormConfig();
  const sidebarRef = React.useRef(null);
  const formFeedbackRef = React.useRef(null);

  return (
    <Container>
      <BaseForm
        onSubmit={() => {}}
        formik={{
          initialValues: record,
          validationSchema: DepositValidationSchema,
          validateOnChange: false,
          validateOnBlur: false,
          enableReinitialize: true,
        }}
      >
        <Grid>
          <Ref innerRef={formFeedbackRef}>
            <Grid.Column
              id="main-content"
              mobile={16}
              tablet={16}
              computer={11}
            >
              <Sticky context={formFeedbackRef} offset={20}>
                <Overridable id="{%- endraw -%}{{cookiecutter.name}}{%- raw -%}.Deposit.FormFeedback.container">
                  <FormFeedback />
                </Overridable>
              </Sticky>
              <TextField
                fieldPath="metadata.title"
                label={
                  <FieldLabel
                    htmlFor="title-field"
                    icon="book"
                    label="Record title"
                  />
                }
                placeholder="Enter a record title"
                required
                className="title-field"
                optimized
                fluid
              />
              <pre>Add more of your deposit form fields here 👇</pre>
              <FormikStateLogger render={true} />
            </Grid.Column>
          </Ref>
          <Ref innerRef={sidebarRef}>
            <Grid.Column
              id="control-panel"
              mobile={16}
              tablet={16}
              computer={5}
            >
              <Sticky context={sidebarRef} offset={20}>
                <Overridable id="{%- endraw -%}{{cookiecutter.name}}{%- raw -%}.Deposit.ControlPanel.container">
                  <Card fluid>
                    {/* <Card.Content>
                      <DepositStatusBox />
                    </Card.Content> */}
                    <Card.Content>
                      <Grid>
                        <Grid.Column
                          computer={8}
                          mobile={16}
                          className="left-btn-col"
                        >
                          <SaveButton fluid />
                        </Grid.Column>

                        <Grid.Column
                          computer={8}
                          mobile={16}
                          className="right-btn-col"
                        >
                          <PreviewButton fluid />
                        </Grid.Column>

                        <Grid.Column width={16} className="pt-10">
                          <PublishButton />
                        </Grid.Column>
                        <Grid.Column width={16} className="pt-10">
                          <ValidateButton />
                        </Grid.Column>
                        {/* TODO:see if there is a better way to provide URL here, seems that UI links are empty in the form */}
                        <Grid.Column width={16} className="pt-10">
                          <DeleteButton redirectUrl="{%- endraw -%}{{cookiecutter.endpoint}}{%- raw -%}" />
                        </Grid.Column>
                      </Grid>
                    </Card.Content>
                  </Card>
                </Overridable>
              </Sticky>
            </Grid.Column>
          </Ref>
        </Grid>
      </BaseForm>
    </Container>
  );
};
{% endraw %}