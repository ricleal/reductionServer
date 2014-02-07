SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `reductiondb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `reductiondb` ;

-- -----------------------------------------------------
-- Table `reductiondb`.`numors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reductiondb`.`numors` ;

CREATE  TABLE IF NOT EXISTS `reductiondb`.`numors` (
  `numor` INT NOT NULL ,
  `filepath` VARCHAR(256) NOT NULL ,
  `intrument_name` VARCHAR(45) NOT NULL ,
  `update_date` DATETIME NOT NULL ,
  PRIMARY KEY (`numor`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reductiondb`.`queries`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reductiondb`.`queries` ;

CREATE  TABLE IF NOT EXISTS `reductiondb`.`queries` (
  `query_id` VARCHAR(36) NOT NULL ,
  `instrument_name` VARCHAR(45) NOT NULL ,
  `update_date` DATETIME NOT NULL ,
  PRIMARY KEY (`query_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reductiondb`.`queries_has_numors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reductiondb`.`queries_has_numors` ;

CREATE  TABLE IF NOT EXISTS `reductiondb`.`queries_has_numors` (
  `query_id` VARCHAR(36) NOT NULL ,
  `numor` INT NOT NULL ,
  PRIMARY KEY (`query_id`, `numor`) ,
  INDEX `fk_queries_has_numors_numors1` (`numor` ASC) ,
  INDEX `fk_queries_has_numors_queries` (`query_id` ASC) ,
  CONSTRAINT `fk_queries_has_numors_queries`
    FOREIGN KEY (`query_id` )
    REFERENCES `reductiondb`.`queries` (`query_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_queries_has_numors_numors1`
    FOREIGN KEY (`numor` )
    REFERENCES `reductiondb`.`numors` (`numor` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
