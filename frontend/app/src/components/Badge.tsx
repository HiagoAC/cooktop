import { v4 as uuidv4 } from 'uuid';
import { CloseButton , Badge as BaseBadge } from 'react-bootstrap';
import styles from '../styles/Badge.module.css';


export interface Props {
    item: string,
    onDelete?: (item: string) => void,
}


export function Badge({ item, onDelete }: Props) {
    return (
        <BaseBadge bg="custom" key={uuidv4()} className={`${styles.custom_badge}`}>
            {item}
            {
                onDelete
                &&
                <CloseButton
                    variant="white"
                    className={`${styles.close_button}`}
                    onClick={() => onDelete(item)}
                />
            }
        </BaseBadge>
    )
}
