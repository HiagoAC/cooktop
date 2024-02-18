import { v4 as uuidv4 } from 'uuid';
import { CloseButton , Badge as BaseBadge } from 'react-bootstrap';
import '../styles/Badge.css';


interface Props {
    item: string,
    withDeleteButton?: boolean,
    onDelete?: (item: string) => void,
}


export function Badge(
    { item, withDeleteButton = false, onDelete = () => {} }
    : Props) {
    return (
        <BaseBadge bg="custom" key={uuidv4()} className="custom-badge">
            {item}
            {
                withDeleteButton
                &&
                <CloseButton
                    variant="white"
                    className="close-button"
                    onClick={() => onDelete(item)}
                />
            }
        </BaseBadge>
    )
}
