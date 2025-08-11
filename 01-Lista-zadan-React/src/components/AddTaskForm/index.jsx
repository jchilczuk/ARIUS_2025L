import {useInput} from '../hooks';


export default function AddTaskForm ({onNewTask = f => f}) {
    const [titleProps, resetTitle] = useInput("");
    const [descriptionProps, resetDescription] = useInput("");
    const [dateProps, resetDate] = useInput("");
    const [timeProps, resetTime] = useInput("");

    
    const submit = event => {
        event.preventDefault();
        const now = new Date();
        const selectedDate = dateProps.value;
        const selectedTime = timeProps.value || '00:00';

        const taskDate = new Date(`${selectedDate}T${selectedTime}`);

        const initialState = taskDate < now ? "Przeterminowane" : "Oczekujące";
        const formattedDate = `${selectedTime} ${selectedDate.split('-').reverse().join('.')}`;

        onNewTask(titleProps.value, descriptionProps.value, formattedDate, initialState);
        resetTitle();
        resetDescription();
        resetDate();
        resetTime();
    };
    
    return (
        <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "300px" }}>
                <input {...titleProps} type="text" placeholder="Nazwa zadania ..." required />
                <input {...descriptionProps} type="text" placeholder="Opis zadania ..."  />
            <div>
                <label>Wybierz godzinę:</label>
                <input {...timeProps} type="time" />
            </div>
            <div>
                <label>Wybierz datę:</label>
                <input {...dateProps} type="date" required />
            </div>
            <div>
                <button>DODAJ</button>
            </div>
        </form>
    );
}


