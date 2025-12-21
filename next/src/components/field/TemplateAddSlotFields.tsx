import { Button, FormLabel, Grid } from "@mui/material";
import { UncontrolledFormField } from "./UncontrolledFields";
import { Field } from "@/utils/types";
import { UncontrolledSelectField } from "./UncontrolledSelectField";
import { TemplateSlot } from "@/types/TemplateType";
import { FormGrid } from "../grid/FormGrid";
export const TemplateAddSlotFields = ({
  group_id,
  defaultValue,
}: {
  group_id: string | null;
  defaultValue: TemplateSlot;
}) => {
  return (
    <Grid container spacing={2}>
      <FormGrid size={3}>
        <FormLabel htmlFor="date_from_start" required>
          何日目
        </FormLabel>
        <UncontrolledFormField
          fieldKey="date_from_start"
          fieldType={Field.NUMBER}
          defaultValue={defaultValue.date_from_start}
        />
      </FormGrid>
      <FormGrid size={6}>
        <UncontrolledFormField
          fieldKey="start_time"
          fieldType={Field.TIME}
          defaultValue={defaultValue.start_time}
        />
      </FormGrid>
      {group_id ? (
        <FormGrid size={3}>
          <FormLabel htmlFor="task_id" required>
            仕事内容
          </FormLabel>
          <UncontrolledSelectField
            fieldKey="task_id"
            defaultValue={defaultValue.task_id}
            params={`group_id=${group_id}`}
          />
        </FormGrid>
      ) : null}
      <Button type="submit" variant="contained" sx={{ mt: 3, mb: 2 }}>
        追加
      </Button>
    </Grid>
  );
};
