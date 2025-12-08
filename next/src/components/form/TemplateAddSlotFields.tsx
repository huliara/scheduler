import { Button, Grid } from "@mui/material";
import { FormField } from "./Form";
import { Field } from "@/utils/types";
import { SelectField } from "./SelectField";
import { TemplateSlot } from "@/types/TemplateType";

export const TemplateAddSlotFields = ({
  group_id,
  defaultValue,
}: {
  group_id: string | null;
  defaultValue: TemplateSlot;
}) => {
  return (
    <Grid container spacing={2}>
      <FormField
        fieldKey="date_from_start"
        fieldType={Field.NUMBER}
        defaultValue={defaultValue.date_from_start}
      />
      <FormField
        fieldKey="start_time"
        fieldType={Field.TIME}
        defaultValue={defaultValue.start_time}
      />
      {group_id ? (
        <SelectField
          fieldKey="task_id"
          defaultValue={defaultValue.task_id}
          params={`group_id=${group_id}`}
        />
      ) : null}
      <Button type="submit" variant="contained" sx={{ mt: 3, mb: 2 }}>
        追加
      </Button>
    </Grid>
  );
};
