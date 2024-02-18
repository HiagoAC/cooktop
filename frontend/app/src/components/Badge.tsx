import { CloseButton , Badge as BaseBadge } from 'react-bootstrap';
import '../styles/Badge.css';


interface BadgeProps {
    item: string,
    withDeleteButton?: boolean
}


export function Badge({ item, withDeleteButton = false }: BadgeProps) {
    return (
        <BaseBadge bg="custom" className="custom-badge">
            {item}
            {withDeleteButton && <CloseButton variant="white" className="close-button"/>}
        </BaseBadge>
    )
}
