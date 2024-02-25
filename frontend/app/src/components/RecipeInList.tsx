import { Link } from 'react-router-dom';
import { Card } from 'react-bootstrap';
import { BadgeStack } from './BadgeStack';
import styles from '../styles/RecipeInList.module.css';
import clockIcon from '../assets/clock_icon.svg';


interface Props {
    id: number,
    title: string,
    time_minutes: number,
    tags: string[],
    image: string
}


export function RecipeInList({ id, title, time_minutes, tags, image }:
    Props) {
        return <Card className={`${styles.recipe_card_container}`}>
            <Card.Img
                variant="top"
                src={image}
                height="150px"
                className={`${styles.card_img}`}
            />
            <Card.Body className="d-flex flex-column" key={id}>
                <Card.Title>{title}</Card.Title>
                <Card.Text>
                    <span>
                        <div className={`${styles.icon_container}`}>
                            <img
                                src={clockIcon}
                                alt="prep time"
                                className={`${styles.clock_icon}`}
                            />
                        </div> {time_minutes} min
                    </span>
                    <BadgeStack items={tags} />
                </Card.Text>
                <Link to={`/recipes/${id.toString()}`} className="stretched-link" />
            </Card.Body>
        </Card>
}
