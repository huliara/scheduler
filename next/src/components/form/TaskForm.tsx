import { TaskResponse } from "@/types/ResponseType";
import {
  Grid,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
} from "@mui/material";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { Dispatch, SetStateAction, useState } from "react";
import CloseIcon from "@mui/icons-material/Close";
import AddIcon from "@mui/icons-material/Add";
export const TaskForm = ({
  data,
  subtasks,
  setSubtasks,
}: {
  data: TaskResponse;
  subtasks: string[];
  setSubtasks: Dispatch<SetStateAction<string[]>>;
}) => {
  const [subtaskText, setSubtaskText] = useState<string>("");
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <TextField
          autoComplete="given-name"
          name="name"
          required
          id="name"
          label="名前"
          autoFocus
          defaultValue={data.name}
        />
      </Grid>
      <Grid item xs={12}>
        <List>
          {subtasks.map((subtask, index) => (
            <ListItem key={index}>
              <ListItemText primary={`${index + 1}. ${subtask}`} />
              <Button
                variant="outlined"
                color="error"
                onClick={() => {
                  setSubtasks(subtasks.filter((_, i) => i !== index));
                }}
              >
                <CloseIcon />
              </Button>
            </ListItem>
          ))}
          <ListItem>
            <TextField
              fullWidth
              label="詳細"
              variant="outlined"
              value={subtaskText}
              onChange={(e) => {
                setSubtaskText(e.target.value);
              }}
            />
            <ListItemButton
              onClick={() => {
                setSubtasks([...subtasks, subtaskText]);
                setSubtaskText("");
              }}
            >
              <AddIcon />
            </ListItemButton>
          </ListItem>
        </List>
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          required
          id="max_worker_num"
          label="最大参加者数"
          name="max_worker_num"
          type="number"
          inputProps={{ min: 1, max: 100, step: 1 }}
          defaultValue={data.max_worker}
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          required
          id="min_worker_num"
          label="最低参加者数"
          name="min_worker_num"
          type="number"
          inputProps={{ min: 0, max: 100, step: 1 }}
          defaultValue={data.min_worker}
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          required
          id="exp_worker_num"
          label="最低経験者数"
          name="exp_worker_num"
          type="number"
          inputProps={{ min: 0, max: 100, step: 1 }}
          defaultValue={data.exp_worker}
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          required
          id="point"
          label="ポイント"
          name="point"
          type="number"
          inputProps={{ min: -100, max: 100, step: 1 }}
          defaultValue={data.wage}
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          required
          id="duration"
          label="所要時間(分)"
          name="duration"
          type="number"
          inputProps={{ min: 0, step: 1 }}
          defaultValue={data.duration}
        />
      </Grid>

      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        保存
      </Button>
    </Grid>
  );
};
